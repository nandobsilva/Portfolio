// EXTERNAL COMPONENTS
import React from "react";
import NavBar from "../components/NavBar";
import RegisterUser from "../components/RegisterUser";

// INTERNAL COMPONENTS
import Footer from "../components/Footer";

export default function CreateUser() {
  return (
    <React.Fragment>
      <NavBar menu={"create"} />
      <RegisterUser />
      <div className="container fixed-bottom mt-4">
        <Footer />
      </div>
    </React.Fragment>
  );
}
