import Login from "./components/Login"
import React, {useContext, useState} from "react";
import './App.css';
import Ambulances from "./components/Ambulances";
import Patients from "./components/Patients"
import Register from "./components/Register";
import Header from "./components/Header";
import Users from "./components/Users"
import MyPanel from "./components/MyPanel";
import {UserContext} from "./context/UserContext";

const App = () => {
    const [token] = useContext(UserContext);
    const [page] = useContext(UserContext);

    let component
    switch (window.location.pathname) {
        case "/":
            component = <Ambulances/>
            break
        case "/patients":
            component = <Patients/>
            break
        case "/ambulances":
            component = <Ambulances/>
            break
        case "/users":
            component = <Users/>
            break
        case "/mypanel":
            component = <MyPanel/>
            break
    }

    return (
      <div className="App">
          <Header title = "Grim Reaper"/>
          <div className="columns" is-centered>
              <div className="column"></div>
              <div className="column" m-5 is-two-thirds >
                  {
                      !token ? (
                          <div className="columns" is-centered>
                                  <Register/> <Login/>
                          </div>
                      ) : (
                          <div>
                          {component}
                          </div>
                      )
                  }
              </div>
              <div className="column"></div>
          </div>
      </div>
  );
}

export default App;
