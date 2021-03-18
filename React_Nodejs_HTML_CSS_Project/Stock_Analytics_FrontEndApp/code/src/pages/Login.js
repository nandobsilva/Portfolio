// EXTERNAL COMPONENT
import React, { useState } from "react";
import Private from "./Private";

// INTERNAL COMPONENT
import NavBar from "../components/NavBar";
import Authentication from "../components/Authentication";
import Footer from "../components/Footer";

export default function Login() {
  const [isLoged, setIsLoged] = useState(false);

  const checkLogin = () => {
    setIsLoged(true);
  };

  // RENDER
  if (isLoged === true) {
    return <Private loged={true} />;
  }
  return (
    <React.Fragment>
      <NavBar menu={"login"} key="title" />
      <Authentication onLogin={checkLogin} />
      <div className="container fixed-bottom mt-4">
        <Footer />
      </div>
    </React.Fragment>
  );
}
