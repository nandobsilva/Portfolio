//EXTERNAL COMPONENTS
import React, { useState } from "react";
import axios from "axios";

// INTERNAL COMPONENTS
import NavBar from "../components/NavBar";
import FilterMenu from "../components/FilterMenu";
import TableStock from "../components/TableStock";
import WelcomeBanner from "../components/WelcomeBanner";
import TableCompaniesFound from "../components/TableCompaniesFound";
import TableCompaniesSelected from "../components/TableCompaniesSelected";
import GetData from "../utilities/GetData";
import Footer from "../components/Footer";
import Main from "./Main";

export default function Private() {
  // VARIABLES
  // Store information selected by the user to render the screen
  const [dataSelected, setDataSelected] = useState([]);
  const [seeCompaniesFound, setSeeCompaniesFound] = useState(true);
  // Store date from the database
  const [dataFromDatabase, setDataFromDatabase] = useState([]);

  // METHODS
  // Set the status of the button search
  const onSearchClick = (data) => {
    if (seeCompaniesFound) setSeeCompaniesFound(false);
    if (!seeCompaniesFound) setSeeCompaniesFound(true);
  };

  // Check if a company is in the array of items selected by the user
  function hasItem(company) {
    for (let i = 0; i < dataSelected.length; i++) {
      if (dataSelected[i].symbol === company.symbol) return true;
    }
    return false;
  }

  // Add a company in the array of items selected by the user
  const onAddCompany = (company) => {
    if (!hasItem(company)) {
      setDataSelected([
        ...dataSelected,
        {
          id: dataSelected.length,
          symbol: company.symbol,
          name: company.name,
          industry: company.industry,
        },
      ]);
      getDataFromDatabase(company);
    }
  };

  // Remove a item from the array of items selected by the user
  const onRemoveCompany = (company) => {
    const companiesSelected = dataSelected.filter(
      (c) => c.symbol !== company.symbol
    );
    const companiesFromDatabase = dataFromDatabase.filter(
      (c) => c.symbol !== company.symbol
    );
    if (dataSelected.length === 1) setSeeCompaniesFound(true);
    setDataSelected(companiesSelected);
    setDataFromDatabase(companiesFromDatabase);
  };

  // Remove all items items selected by the user
  const onRemoveAll = () => {
    const companiesSelected = [];
    const companiesFromDatabase = [];
    setDataSelected(companiesSelected);
    setDataFromDatabase(companiesFromDatabase);
    if (seeCompaniesFound === false) {
      onSearchClick();
      onSetIndustry(uniqueIndustry[0]);
    }
  };

  // -------------------------------- DATABASE ----------------------------------------
  /*
  GET AND FORMAT DATA FROM THE DATABASE AND STORA IN THE VARIABLE "dataFromDatabase"
  */
  //------------------------------------------------------------------------------------
  // Add data from the database to a local variable
  const onAddCompanyFromDatabase = (data) => {
    let rawData = dataFromDatabase.sort();

    // Use to format number
    const formatter = new Intl.NumberFormat("en");
    // Set data from the database in the variable "dataFromDatabase"
    for (let i = 0; i < data.length; i++) {
      const date = new Date(data[i].timestamp);
      const dateFormated =
        date.getDate().toString() +
        "/" +
        (date.getMonth() + 1).toString() +
        "/" +
        date.getFullYear().toString();

      //const timestamp = date.toLocaleDateString("en-AU");
      // Number Format
      const open = formatter.format(data[i].open);
      const high = formatter.format(data[i].high);
      const low = formatter.format(data[i].low);
      const close = formatter.format(data[i].close);
      const volume = formatter.format(data[i].volumes);
      // Add data from the database to a local variable
      rawData.push({
        id: rawData.length,
        timestamp: date,
        date: dateFormated,
        symbol: data[i].symbol,
        name: data[i].name,
        industry: data[i].industry,
        open: open,
        high: high,
        low: low,
        close: close,
        volumes: volume,
      });
    }
    setDataFromDatabase(rawData);
  };

  // Authentication token to the database
  const config = {
    headers: {
      accept: "application/json",
      "Content-Type": "application/json",
      Authorization: `Bearer ${localStorage.getItem("token")}`,
    },
  };

  // Default dates to execute the search
  let from = "2019-11-06";
  let to = new Date();

  // Fetch data from the database
  const getDataFromDatabase = (company) => {
    let url = `http://131.181.190.87:3000/stocks/authed/${company.symbol}?from=${from}&to=${to}`;
    axios
      .get(url, config)
      .then((res) => res.data)
      .then((data) => {
        onAddCompanyFromDatabase(data);
      })
      .catch((e) => {
        console.log(e);
        alert(e);
      });
  };

  //-------------------------------------- FILTERS  ---------------------------------------
  /*
    VARIABLE AND METHODS TO FILTER AND STORE DATA ACCODING WITH THE USER SELECTION
  */
  //----------------------------------------------------------------------------------------
  // VARIABLES
  const { data, loading, uniqueIndustry, error } = GetData();
  const [name, setName] = useState("");
  const [symbol, setSymbol] = useState("");
  const [industry, setIndustry] = useState(uniqueIndustry[0]);
  const [currentPage, setCurrentPage] = useState(1);
  const numberOfRows = 15;

  // METHODS
  // Sete status of the above variables (name, symbol, industry)
  const onSetIndustry = (e) => {
    setIndustry(e);
    setCurrentPage(1);
  };
  const onSetName = (e) => {
    setName(e);
    setCurrentPage(1);
  };
  const onSetSymbol = (e) => {
    setSymbol(e);
    setCurrentPage(1);
  };
  function onPageChange(page) {
    setCurrentPage(page);
  }

  // Filter the table according with the user selections
  var dataFiltered = data;
  if (symbol !== "") {
    dataFiltered = dataFiltered
      .sort()
      .filter((item) => item.symbol.includes(symbol.toUpperCase()));
  }
  if (name !== "") {
    dataFiltered = dataFiltered
      .sort()
      .filter((item) => item.name.toUpperCase().includes(name.toUpperCase()));
  }
  if (industry !== "" && industry !== "All industries") {
    dataFiltered = dataFiltered
      .sort()
      .filter((item) =>
        item.industry.toUpperCase().includes(industry.toUpperCase())
      );
  }

  // RENDER
  if (localStorage.getItem("token") === null) {
    return <Main />;
  }

  return (
    <React.Fragment>
      <NavBar menu={"private"} />
      {seeCompaniesFound === true && <WelcomeBanner />}
      <div>
        <TableCompaniesSelected
          dataSelected={dataSelected}
          onRemoveCompany={onRemoveCompany}
          onSearchClick={onSearchClick}
          onRemoveAll={onRemoveAll}
          seeCompaniesFound={seeCompaniesFound}
        />
        {seeCompaniesFound === true && (
          <div>
            <FilterMenu
              data={data}
              loading={loading}
              error={error}
              onSetName={onSetName}
              onSetSymbol={onSetSymbol}
              onSetIndustry={onSetIndustry}
              uniqueIndustry={uniqueIndustry}
              name={name}
              symbol={symbol}
              industry={industry}
            />

            <TableCompaniesFound
              data={dataFiltered}
              onAddCompany={onAddCompany}
              dataSelected={dataSelected}
              onPageChange={onPageChange}
              currentPage={currentPage}
            />
          </div>
        )}
      </div>
      <div>
        {seeCompaniesFound === false && (
          <div>
            <TableStock
              dataFromDatabase={dataFromDatabase}
              onSearchClick={onSearchClick}
              numberOfRows={numberOfRows}
              dataSelected={dataSelected}
              seeCompaniesFound={seeCompaniesFound}
            />
          </div>
        )}
        <Footer />
      </div>
    </React.Fragment>
  );
}
