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
import ChartPublic from "../components/ChartPublic";

export default function Main() {
  // CLEAN ANY POSSIBLE TOKE IN THE LOCAL STORAGE
  localStorage.removeItem("token");

  // VARIABLES
  //USED TO STORE INFORMATION SELECTED BY THE USER AND DEFINE COMPONENTS ON THE SCREEN
  const [dataSelected, setDataSelected] = useState([]);
  const [dataFromDatabase, setDataFromDatabase] = useState([]);
  const [seeCompaniesFound, setSeeCompaniesFound] = useState(true);

  // METHODS
  // Set the status of the button search
  const onSearchClick = () => {
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
    }
  };

  // Format the number retrieved from the database
  const formatter = new Intl.NumberFormat("en");

  //-------------------------------- DATA BASE CONNECTION ----------------------------
  // Fetch data from the database
  const getDataFromDatabase = (company) => {
    axios
      .get(`http://131.181.190.87:3000/stocks/${company.symbol}`)
      .then((res) => res.data)
      .then((res) => {
        // Date format
        let date = new Date(res.timestamp);
        const timestamp = date.toLocaleDateString("en-AU");
        const dateFormated =
          date.getDate().toString() +
          "/" +
          (date.getMonth() + 1).toString() +
          "/" +
          date.getFullYear().toString();

        // Number Format
        const open = formatter.format(res.open);
        const high = formatter.format(res.high);
        const low = formatter.format(res.low);
        const close = formatter.format(res.close);
        const volume = formatter.format(res.volumes);

        setDataFromDatabase([
          ...dataFromDatabase,
          {
            timestamp: timestamp,
            date: dateFormated,
            symbol: res.symbol,
            name: res.name,
            industry: res.industry,
            open: open,
            high: high,
            low: low,
            close: close,
            volumes: volume,
          },
        ]);
      })
      .catch((e) => {
        console.log(e);
        console.log("GetDataBySymbol: " + e.message);
        alert(e);
      });
  };

  //----------------- VARIABLES AND METHODS USED BY THE FILTER COMPONENT --------------
  // VARIABLES
  const { data, loading, uniqueIndustry, error } = GetData();
  const [name, setName] = useState("");
  const [symbol, setSymbol] = useState("");
  const [industry, setIndustry] = useState(uniqueIndustry[0]);
  const [currentPage, setCurrentPage] = useState(1);

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
  //-------------------------------------------------------------------------------------

  return (
    <React.Fragment>
      <NavBar menu={"main"} />
      <WelcomeBanner />

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
              dataSelected={dataSelected}
            />
            <br />
            <ChartPublic data={dataFromDatabase} />
          </div>
        )}
      </div>
      <Footer />
    </React.Fragment>
  );
}
