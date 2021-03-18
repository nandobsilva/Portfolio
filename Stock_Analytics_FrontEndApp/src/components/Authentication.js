// EXTERNAL COMPONENT
import React, { useState } from "react";
import axios from "axios";

export default function Login(props) {
  const { onLogin } = props;

  // Authentication method
  const URL = "http://131.181.190.87:3000/user/login";
  const [user, setUser] = useState({ email: "", password: "" });
  const submitPost = (e) => {
    e.preventDefault();
    axios
      .post(URL, user)
      .then((res) => res.data)
      .then((data) => {
        localStorage.setItem("token", data.token);
        localStorage.setItem("hasToken", "true");
        localStorage.setItem("user", user.email);
        onLogin(true);
      })
      .catch((error) => {
        console.log(error);
        alert(" Invalid user or password!\n\tPlease try it again.");
      });
  };

  // Render
  return (
    <div>
      <div className="container">
        <div className="row">
          <div className="col"></div>
          <div className="col mt-5">
            <div className="row justify-content-center ">
              <img
                src="https://designmyschool.com.au/sites/default/files/images/template/circle-account.png"
                alt=""
                style={{ width: "100px", height: "100px" }}
              />
            </div>
            <div className="row justify-content-center mt-5">
              <form
                className="form-inline"
                onSubmit={(e) => {
                  e.preventDefault();
                }}
              >
                <input
                  className="form-control "
                  type="email"
                  placeholder="E-mail"
                  id="email"
                  value={user.email}
                  onChange={(e) => setUser({ ...user, email: e.target.value })}
                />
              </form>
            </div>
            <div className="row justify-content-center mt-4">
              <form
                className="form-inline my-1 my-lg-0"
                onSubmit={(e) => {
                  e.preventDefault();
                }}
              >
                <input
                  className="form-control "
                  type="password"
                  placeholder="Password"
                  id="password"
                  value={user.password}
                  onChange={(e) =>
                    setUser({ ...user, password: e.target.value })
                  }
                />
              </form>
            </div>
            <div className="row justify-content-center mt-4">
              <form className="form-inline ">
                <button className="btn btn-dark btn-block" onClick={submitPost}>
                  Login
                </button>
              </form>
            </div>
          </div>
          <div className="col-sm"></div>
        </div>
      </div>
    </div>
  );
}
