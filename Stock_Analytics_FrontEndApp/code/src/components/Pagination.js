import React from "react";
import _ from "lodash";

export default function Pagination(props) {
  const { data, dataSelected, onPageChange, currentPage, pageSize } = props;

  // DEFINE THE SIZE OF THE PAGE
  const pagesCount = (data.length - dataSelected.length) / pageSize;
  const pages = _.range(1, pagesCount + 1);

  if (pagesCount <= 1) return null;

  return (
    <nav>
      <ul className="pagination pagination-sm justify-content-center">
        {pages.map((page) => (
          <li
            key={page}
            className={page === currentPage ? "paga-item active" : "page-item"}
          >
            <button className="page-link  " onClick={() => onPageChange(page)}>
              {page}
            </button>
          </li>
        ))}
      </ul>
      <hr />
    </nav>
  );
}
