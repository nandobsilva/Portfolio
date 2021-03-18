import React from "react";
import { Route, Switch, Redirect } from "react-router-dom";

//INTERNAL MODULES
import Main from "./pages/Main";
import CreateUser from "./pages/CreateUser";
import Contact from "./pages/Contact";
import Logout from "./pages/Logout";
import Login from "./pages/Login";
import Private from "./pages/Private";

function App() {
  return (
    <React.Fragment>
      <div className="container">
        <div className="content">
          <Switch>
            <Route path="/main" component={Main} />
            <Route path="/private" component={Private} />
            <Route path="/create" component={CreateUser} />
            <Route path="/contact" exact component={Contact} />
            <Route path="/login" component={Login} />
            <Route path="/logout" component={Logout} />
            <Redirect from="/" to="/main" />
          </Switch>
        </div>
      </div>
    </React.Fragment>
  );
}

export default App;
