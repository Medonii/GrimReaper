import React, {useContext, useState} from 'react';
import {UserContext, UserProvider} from "../context/UserContext";
import gr_logofull from "../gr_logofull.png"
import Navbar from "./Navbar";
import '../styles/Navbar.css';


const Header = () => {
    const [token, setToken] = useContext(UserContext);
    const [, setRole] = useState(localStorage.getItem('role'));
    const [, setAmbulance] = useState(localStorage.getItem('ambulance'));
    const [nickname] = useState(localStorage.getItem('ID'));

    const handleLogout = () => {
        setToken(null);
        setAmbulance(null);
        setRole(null);
    };


    return (

        <div className="has-text-centered m-6">
            {
                !token ? (
                    <h1 className="title">
                        <img src={gr_logofull} className="App-logo" alt="logo" />
                    </h1>
                ) : (
                    <h1 className="title" >
                        <div className="has-text-left">
                            <img src={gr_logofull} className="App-logo" alt="logo"/>
                            <div className="columns" color="lightgrey">
                                <div>Welcome {nickname}</div>
                                <button className="button mt-5 ml-5" style={{position: "absolute", right: 10}}onClick={handleLogout}>
                                Logout
                                </button>
                            </div>
                        </div>
                    </h1>
                )
            }

            {token && (
                <div className="columns is-">
                <Navbar/>
                </div>
            )}
        </div>
    );
};

export default Header;