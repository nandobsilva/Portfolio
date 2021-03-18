// EXTERNAL COMPONENTS
import React from "react";
import { Badge } from "reactstrap";

export default function CompaniesSelected(props) {
  const {
    dataSelected,
    onRemoveCompany,
    onSearchClick,
    onRemoveAll,
    seeCompaniesFound,
  } = props;

  // RENDER
  return (
    <div>
      {dataSelected.length > 0 && (
        <div>
          <div className="row">
            <div className="col-sm">
              <br />
              <h4>
                <Badge color="info">{dataSelected.length}</Badge> Companies
                selected.
              </h4>
              <table className="table table-sm">
                <thead className="thead-light">
                  <tr>
                    <th scope="col">Symbol</th>
                    <th scope="col">Company name</th>
                    <th scope="col">Industry</th>
                    <th style={{ textAlign: "right" }} scope="col">
                      Selection
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {dataSelected.map((company) => (
                    <tr key={company.symbol}>
                      <td>{company.symbol}</td>
                      <td>{company.name}</td>
                      <td>{company.industry}</td>
                      <td style={{ textAlign: "right" }}>
                        <button
                          className="btn btn-danger btn-sm"
                          onClick={() => onRemoveCompany(company)}
                        >
                          Remove
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
          <div className="row">
            <div className="col"></div>
            <div className="col"></div>
            <div className="col">
              <div className="col"></div>
            </div>
            <div>
              <div className="col" style={{ textAlign: "right" }}>
                {seeCompaniesFound && (
                  <button
                    className=" btn btn-info  mr-3"
                    onClick={onSearchClick}
                  >
                    SEARCH
                  </button>
                )}
                {!seeCompaniesFound && (
                  <button
                    className=" btn btn-info mr-3"
                    onClick={onSearchClick}
                  >
                    GO BACK
                  </button>
                )}
                <button className=" btn btn-danger" onClick={onRemoveAll}>
                  REMOVE ALL
                </button>
              </div>
            </div>
          </div>
          <hr />
        </div>
      )}
    </div>
  );
}
