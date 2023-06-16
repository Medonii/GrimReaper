import React, {createContext, useEffect, useState} from "react";

export const UserContext = createContext();

export const UserProvider = (props) => {
    const [token, setToken] = useState(localStorage.getItem("grimToken"));
    const [ambulance, setAmbulance] = useState(localStorage.getItem("ambulance"))
    const [role, setRole] = useState(localStorage.getItem("role"))
    const [nickname, setNickname] = useState(localStorage.getItem("ID"))

    useEffect(() => {
            const fetchUser = async () => {
                const requestOptions = {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: "Bearer " + token,
                    },
                };
                    const response = await fetch("http://user-service:8888/users/me", requestOptions);

                    if(!response.ok) {
                        setToken(null);
                        setAmbulance(null);
                        setRole(null);
                        setNickname(null);
                    }
                        localStorage.setItem("grimToken", token);
                        const data = await response.json();
                        localStorage.setItem("ambulance", data.ambulance);
                        localStorage.setItem("ID", data.nickname);
                        localStorage.setItem("role", data.role);
            };
            fetchUser();
        },
        [token]);

    return (
        <UserContext.Provider value={[token, setToken]}>
            {props.children}
        </UserContext.Provider>
    )
}