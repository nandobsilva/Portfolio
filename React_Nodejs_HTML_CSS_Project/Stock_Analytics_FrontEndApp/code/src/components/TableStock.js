// EXTERNAL COMPONENT
import React, { useState } from "react";
import { AgGridReact } from "ag-grid-react";
import "ag-grid-community/dist/styles/ag-grid.css";
import "ag-grid-community/dist/styles/ag-theme-balham.css";
import { Badge } from "reactstrap";
import DatePicker from "react-datepicker";

// INTERNAL COMPONENTS
import ChartPrivate from "../components/ChartPrivate";

export default function TableStock(props) {
  // VARIABLES
  const { dataFromDatabase, dataSelected } = props;
  // Define the min and max date
  if (dataFromDatabase.length !== 0) {
    var minDate = firstDate();
    var maxDate = lastDate();
  }
  // Store information selected by the user to render the screen
  const [initialDate, setInitialDate] = useState(minDate);
  const [finalDate, setFinalDate] = useState(maxDate);
  const [companyName, setCompanyName] = useState("All companies");

  // Set the initial and final date for the search
  const onSetFinalDate = (date) => {
    setFinalDate(date);
  };
  const onSetInitialDate = (date) => {
    setInitialDate(date);
  };

  const onSetCompanyName = (data) => {
    setCompanyName(data);
  };

  const onReset = () => {
    setInitialDate(minDate);
    setFinalDate(maxDate);
  };

  // Initial and final dates from the database data.

  function firstDate() {
    const data = dataFromDatabase;
    let firstDate = data[0].timestamp;
    for (let i = 0; i < data.length - 1; i++) {
      if (data[i + 1].timestamp < firstDate) firstDate = data[i + 1].timestamp;
    }
    return firstDate;
    //setMinDate(firstDate);
  }
  function lastDate() {
    const data = dataFromDatabase;
    let lastDate = data[0].timestamp;
    for (let i = 0; i < data.length - 1; i++) {
      if (data[i + 1].timestamp > lastDate) lastDate = data[i + 1].timestamp;
    }
    return lastDate;
    //setMaxDate(lastDate);
  }

  // Table columns names
  const columns = [
    {
      headerName: "Date",
      field: "date",
      sortable: false,
      width: 110,
      resizable: true,
      filter: true,
    },
    {
      headerName: "Symbol",
      field: "symbol",
      sortable: true,
      resizable: true,
      width: 70,
    },
    { headerName: "Company", field: "name", sortable: true, resizable: true },
    {
      headerName: "Industry",
      field: "industry",
      sortable: true,
      resizable: true,
    },
    {
      headerName: "Open",
      field: "open",
      sortable: true,
      resizable: true,
      width: 75,
    },
    {
      headerName: "High",
      field: "high",
      sortable: true,
      resizable: true,
      width: 75,
    },
    {
      headerName: "Low",
      field: "low",
      sortable: true,
      resizable: true,
      width: 75,
    },
    {
      headerName: "Close",
      field: "close",
      sortable: true,
      resizable: true,
      width: 75,
    },
    {
      headerName: "Volume",
      field: "volumes",
      sortable: true,
      resizable: true,
      width: 90,
    },
  ];
  // Fiilter data retrieved from the database
  let dataFiltered = dataFromDatabase;
  if (localStorage.getItem("token") !== null) {
    if (initialDate !== minDate) {
      dataFiltered = dataFiltered.filter((c) => c.timestamp >= initialDate);
    }
    if (finalDate !== maxDate) {
      dataFiltered = dataFiltered.filter((c) => c.timestamp <= finalDate);
    }
    if (companyName !== "All companies") {
      dataFiltered = dataFiltered.filter((c) => c.name === companyName);
    }
  }
  dataFiltered = dataFiltered.sort((a, b) => a.timestamp > b.timestamp);

  // Define number of rows in the tables
  let tablesRows = 15;
  if (dataFiltered.length < 15) tablesRows = dataFiltered.length;

  // Define the height of the table
  let height = 120 + dataFromDatabase.length * 25;
  if (localStorage.getItem("token") !== null) height = 500;

  // RENDER
  return (
    <div className="color1">
      <div>
        {localStorage.getItem("token") !== null && (
          <ChartPrivate dataFiltered={dataFiltered} />
        )}
        <hr />

        <h2 className="font5">STOCK PRICES</h2>
      </div>
      <div></div>
      <div>
        <div className="color1">
          {localStorage.getItem("token") !== null && (
            <label className="font1">Filters</label>
          )}
          <div className="row">
            <div className="col">
              {localStorage.getItem("token") !== null && (
                <DatePicker
                  className="dateLabelSize"
                  placeholderText="Inicial date"
                  selected={initialDate}
                  onChange={(date) => onSetInitialDate(date)}
                  minDate={minDate}
                  maxDate={maxDate}
                  dateFormat="dd/MM/yyyy"
                />
              )}
            </div>
            <div className="col">
              {localStorage.getItem("token") !== null && (
                <DatePicker
                  className="dateLabelSize"
                  placeholderText="Final date"
                  selected={finalDate}
                  onChange={(date) => onSetFinalDate(date)}
                  dateFormat="dd/MM/yyyy"
                  minDate={minDate}
                  maxDate={maxDate}
                />
              )}
            </div>
            <div className="col-4">
              {localStorage.getItem("token") !== null && (
                <select
                  className="custom-select mt-2"
                  onChange={(e) => onSetCompanyName(e.target.value)}
                >
                  <option select="true">All companies</option>
                  {dataSelected.map((item) => (
                    <option key={item.symbol}>{item.name}</option>
                  ))}
                </select>
              )}
            </div>
            <div className="col-2" style={{ textAlign: "right" }}>
              {localStorage.getItem("token") !== null && (
                <button className=" btn btn-info mt-2" onClick={onReset}>
                  RESET DATES
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
      <br />
      <p>
        <Badge color="success">{dataFiltered.length}</Badge> Items found.
      </p>
      <div
        className="ag-theme-balham"
        style={{ height: height + "px", width: "1090px" }}
      >
        <AgGridReact
          suppressColumnVirtualisation={true}
          columnDefs={columns}
          rowData={dataFiltered}
          pagination={true}
          paginationPageSize={tablesRows}
        />
      </div>
    </div>
  );
}
