//EXTERNAL COMPONENTS
import React from "react";
import { Link } from "react-router-dom";

export default function Welcome() {
  // RENDER
  return (
    <div className="color3">
      <div className="row ">
        <div className="col-sm "></div>
        <div className="col-6 ">
          <div className="card-body">
            {localStorage.getItem("token") === null && (
              <Link className="nav-link" to={"/create"}>
                <h2 className="font3">WELCOME TO STOCKS ANALYTICS</h2>
                <h4 className="textCenter"> Sign up and have full access</h4>
              </Link>
            )}
            {localStorage.getItem("token") !== null && (
              <div>
                <h2 className="font3">WELCOME </h2>
                <h4 className="font4">{localStorage.getItem("user")}</h4>
              </div>
            )}
          </div>
        </div>
        <div className="col-sm "></div>
      </div>
    </div>
  );
}
