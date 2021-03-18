import React, { useState } from "react";
import axios from "axios";

export default function Register() {
  const URL = "http://131.181.190.87:3000/user/register";
  const [user, setUser] = useState({ email: "", password: "" });

  // Method to register user
  const submitPost = (e) => {
    e.preventDefault();
    axios
      .post(URL, user)
      .then((response) => {
        alert(
          "\t\t\tAccount created.\nPlease go to the login page to authentication."
        );
        // setHasUser(true);
      })
      .catch((error) => {
        //setError(error.message);
        if (error.message.includes("400"))
          alert("Please enter a valid user and password.");

        if (error.message.includes("409"))
          alert("E-mail already exists!  \nPlease enter another e-mail.");
      });
  };

  // RENDER
  return (
    <div className="container">
      <div className="row justify-content-center">
        <div className="col-4 mt-5 ">
          <div className="row justify-content-center mt-5 ">
            <img
              src="https://www.paidmembershipspro.com/wp-content/uploads/2017/07/member-add-on-300x300.png"
              alt=""
              style={{ width: "100px", height: "100px" }}
            />
          </div>
          <div className="row justify-content-center">
            <p className="font2">Create account</p>
          </div>
          <div className="row justify-content-center">
            <form>
              <input
                type="email"
                className="form-control"
                id="email"
                placeholder="E-mail"
                value={user.email}
                onChange={(e) => setUser({ ...user, email: e.target.value })}
              />
            </form>
          </div>
          <br />
          <div className="row justify-content-center">
            <form
              onSubmit={(e) => {
                e.preventDefault();
              }}
            >
              <input
                type="password"
                className="form-control"
                id="password"
                placeholder="Password"
                value={user.password}
                onChange={(e) => setUser({ ...user, password: e.target.value })}
              />
            </form>
          </div>
          <br />
          <div className="row justify-content-center mb-4">
            <button className="btn btn-dark" onClick={submitPost}>
              Sign up
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
