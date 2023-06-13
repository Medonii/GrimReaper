import 'bulma/css/bulma.min.css';
import React, {useState, useContext} from "react";
import {UserContext} from "../context/UserContext";
import ErrorMessage from "./ErrorMessage";


const Register = () => {
    const [nickname, setNickname] = useState("");
    const [password, setPassword] = useState("");
    const [confirmationPassword, setConfirmationPassword] = useState("");
        const [errorMessage, setErrorMessage] = useState("");
        const [,setToken] = useContext(UserContext);

        const submitRegistration = async () => {

            const urlencoded = new URLSearchParams();
            urlencoded.append("username", nickname);
            urlencoded.append("password", password);

            const requestOptions = {
                method: "POST",
                mode: "cors",
                headers: {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"},
                body: urlencoded,
                redirect: "follow"
            };

            const response = await fetch("http://user-service:80/register", requestOptions)
                const data = await response.json();

            if(!response.ok) {
                setErrorMessage(data.detail);
                alert("Error: " + data)
                console.log(response);
            } else
                setToken(data.access_token);
                alert("Success!");
                console.log(response);
        };

        const handleSubmit = (e) => {
            e.preventDefault();
            if(password === confirmationPassword && password.length >5) {
                submitRegistration();
            } else {
                setErrorMessage(
                    "Password is too short or passwords don't match"
                );
            }
        };

        return (
            <div className="column">
                <form className="box" onSubmit={handleSubmit}>
                    <h1 className="title has-text-centered">Register</h1>
                    <div className="field">
                        <label className="label">Nickname</label>
                        <div className="control">
                            <input
                                type="nickname"
                                placeholder="Provide nickname"
                                value={nickname}
                                    onChange={(e)=>setNickname(e.target.value)}
                                    className="input"
                                    required
                            />
                        </div>
                        <div className="field">
                            <label className="label">Password</label>
                            <div className="control">
                            <input
                                type="password"
                                placeholder="Provide password"
                                value={password}
                                onChange={(e)=>setPassword(e.target.value)}
                                className="input"
                                required
                            />
                            </div>
                        </div>
                        <div className="field">
                            <label className="label">Confirmation Password</label>
                            <div className="control">
                            <input
                                type="password"
                                placeholder="Confirm password"
                                value={confirmationPassword}
                                onChange={(e)=>setConfirmationPassword(e.target.value)}
                                className="input"
                                required
                            />
                            </div>
                        </div>
                    </div>
                    <ErrorMessage message = {errorMessage}/>
                    <br/>
                    <button className="button is-primary" type="submit">Register</button>
                </form>
            </div>
        )

}

export default Register;
