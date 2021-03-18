// EXTERNAL COMPONENTS
import React from "react";
import { Badge } from "reactstrap";

// INTERNAL COMPONENTS
import Pagination from "./Pagination";
import { paginate } from "../utilities/UtilPagination";

export default function CompaniesFound(props) {
  const { data, onAddCompany, dataSelected, onPageChange, currentPage } = props;
  const pageSize = 15;

  // METHODS
  /* CHECK IF THE COMPANY IS IN "dataSelected" VARIABLE, IF TRUE THE RENDER DO NOT 
  SHOW THE COMPANY IN THE LIST COMPANIES FOUND
  */
  function isInDataSelected(item) {
    for (let i = 0; i < dataSelected.length; i++) {
      if (dataSelected[i].symbol === item.symbol) {
        return true;
      }
    }
    return false;
  }

  // PAGINATE DATA FROM COMPANIES FOUND
  const companiesPaginated = paginate(data, currentPage, pageSize);

  // RENDER
  return (
    <div>
      <div className="row">
        <div className="col">
          <div>
            <br />
            <div className="row">
              <div className="col">
                <h4 className="font5">
                  <Badge color="warning">{data.length}</Badge> Companies listed
                </h4>
              </div>
            </div>
            <div className="row">
              <div className="col text-right">
                <p>
                  Page <Badge color="warning">{currentPage}</Badge>
                </p>
              </div>
            </div>
            <table className="table table-sm">
              <thead className="thead-dark">
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
                {companiesPaginated.map(
                  (item) =>
                    isInDataSelected(item) === false && (
                      <tr key={item.symbol}>
                        <td>{item.symbol}</td>
                        <td>{item.name}</td>
                        <td>{item.industry}</td>
                        <td style={{ textAlign: "right" }}>
                          <button
                            className="btn btn-info btn-sm"
                            onClick={() => onAddCompany(item)}
                          >
                            Add
                          </button>
                        </td>
                      </tr>
                    )
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
      <br />
      <br />
      <Pagination
        data={data}
        dataSelected={dataSelected}
        onPageChange={onPageChange}
        currentPage={currentPage}
        pageSize={pageSize}
      />
    </div>
  );
}
