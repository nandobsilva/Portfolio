import React from "react";
import { Link } from "react-router-dom";

export default function NavBar(props) {
  // Variables to define the navegation bar titles and links in each page
  const menuLogin = [
    { id: 1, title: "HOME", link: "/" },
    { id: 2, title: "SIGNUP", link: "/create" },
    { id: 3, title: "CONTACT", link: "/contact" },
  ];
  const menuCreateUser = [
    { id: 1, title: "HOME", link: "/" },
    { id: 2, title: "LOGIN", link: "/login" },
    { id: 3, title: "CONTACT", link: "/contact" },
  ];

  const menuContactPublic = [
    { id: 1, title: "HOME", link: "/" },
    { id: 2, title: "LOGIN", link: "/" },
    { id: 3, title: "SIGN UP", link: "/create" },
  ];

  const menuContactPrivate = [
    { id: 1, title: "HOME", link: "/private" },
    { id: 2, title: "LOG OUT", link: "/logout" },
  ];

  const menuMain = [
    { id: 1, title: "LOGIN", link: "/login" },
    { id: 2, title: "SIGN UP", link: "/create" },
    { id: 3, title: "CONTACT", link: "/contact" },
  ];

  const menuDataPrivate = [
    { id: 1, title: "CONTACT", link: "/contact" },
    { id: 3, title: "LOG OUT", link: "/logout" },
  ];

  // METHODS
  // Define the navigation bar in each page according with the props
  function renderMenu() {
    if (props.menu === "login") return menuLogin;
    if (props.menu === "create") return menuCreateUser;
    if (props.menu === "contactPublic") return menuContactPublic;
    if (props.menu === "contactPrivate") return menuContactPrivate;
    if (props.menu === "main") return menuMain;
    if (props.menu === "private") return menuDataPrivate;
    return null;
  }
  const menuNav = renderMenu();

  // RENDER
  return (
    <div className="color2">
      <nav className="navbar navbar-expand-sm navbar-dark ">
        <div className="collapse navbar-collapse" id="navbarSupportedContent">
          <ul className="navbar-nav mr-auto">
            {menuNav.map((item) => (
              <li className="nav-item active" key={item.id}>
                <Link className="nav-link" to={item.link}>
                  {item.title}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      </nav>
    </div>
  );
}
