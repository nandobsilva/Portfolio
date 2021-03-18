// EXTERNAL COMPONENTS
import React from "react";
import "react-datepicker/dist/react-datepicker.css";

// INTERNAL COMPONENTS
import Loading from "../components/Loading";

export default function FilterMenu(props) {
  // VARIABLES USED TO GET THE FILTER PARAMETERS ENTERED BY THE USER
  const {
    loading,
    uniqueIndustry,
    error,
    onSetName,
    onSetSymbol,
    onSetIndustry,
    name,
    symbol,
    industry,
  } = props;

  // ERROR MESSAGE
  if (error !== null) {
    alert("Server not connected. Please try again later.");
    console.log("Location Filter.js: Error - " + error);
  }
  // LOADIN MESSAGE
  if (loading === true) {
    return <Loading />;
  }

  // RENDER
  return (
    <div>
      <div className="color1">
        <hr />
        <label className="font1">Filters</label>
        <div className="Container">
          <div className="row">
            <div className="col-3">
              <form className="form-inline my-2 my-lg-0">
                <input
                  className="form-control mr-sm-2"
                  type="text"
                  placeholder="Contains company symbol"
                  value={symbol}
                  onChange={(e) => onSetSymbol(e.target.value)}
                />
              </form>
            </div>
            <div className="col-3">
              <div>
                <form className="form-inline my-2 my-lg-0">
                  <input
                    className="form-control mr-sm-2"
                    type="text"
                    placeholder="Contains company name"
                    value={name}
                    onChange={(e) => onSetName(e.target.value)}
                  />
                </form>
              </div>
            </div>
            <div className="col">
              <select
                className="custom-select "
                value={industry}
                onChange={(e) => onSetIndustry(e.target.value)}
              >
                {uniqueIndustry.map((item) => (
                  <option key={item}>{item}</option>
                ))}
              </select>
            </div>
          </div>
        </div>
        <hr />
      </div>
    </div>
  );
}
