// EXTERNAL COMPONENTS
import React from "react";
import Main from "../pages/Main";

export default function Logout() {
  localStorage.removeItem("token");
  return (
    <div>
      <Main />
    </div>
  );
}
