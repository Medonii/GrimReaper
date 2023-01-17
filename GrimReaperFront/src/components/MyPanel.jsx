import React, {useContext, useState, useEffect} from 'react';
import ErrorMessage from "./ErrorMessage";
import {UserContext} from "../context/UserContext";

const MyPanel = () => {
    const [token] = useContext(UserContext);
    const [patients,setPatients] = useState(null);
    const [errorMessage, setErrorMessage] = useState("");
    const [loaded, setLoaded] = useState(false);
    const [, setId] = useState(null);
    const [ambulance] = useState(localStorage.getItem("ambulance"))

    const handleReject = async (id) => {
        const requestOptions = {
            method: "PUT",
            headers: {"Content-Type": "application/json",
                        Authorization: "Bearer " + token},
        };
        const response = await fetch(`http://localhost:8080/patients/reject/${id}`, requestOptions);
        if(!response.ok) {
            setErrorMessage("Failed to reject patient")
        } else {
            getMyPatients();
        }
    }

    const handleAccept = async (id) => {
        const requestOptions = {
            method: "PUT",
            headers: {"Content-Type": "application/json",
                        Authorization: "Bearer " + token},
        };
        const response = await fetch(`http://localhost:8008/accept/${id}`, requestOptions);
        if(!response.ok) {
            setErrorMessage("Failed to accept patient request")
        } else {
            getMyPatients();
        }
    }

    const handleStart = async (id) => {
        const requestOptions = {
            method: "PUT",
            headers: {"Content-Type": "application/json",
                        Authorization: "Bearer " + token},
        };
        const response = await fetch(`http://localhost:8080/patients/start/${id}`, requestOptions);
        if(!response.ok) {
            setErrorMessage("Failed to start work on patient")
        } else {
            getMyPatients();
        }
    }

    const handleFinish = async (id) => {
        const requestOptions = {
            method: "PUT",
            headers: {"Content-Type": "application/json",
                        Authorization: "Bearer " + token},
        };
        const response = await fetch(`http://localhost:8080/patients/close/${id}`, requestOptions);
        if(!response.ok) {
            setErrorMessage("Failed to close work on patient")
        } else {
            getMyPatients();
        }
    }

    const getMyPatients = async() => {
        const requestOptions = {
            method: "GET",
            headers: {"Content-Type": "application/json",
                        Authorization: "Bearer " + token},
        };
        const response = await fetch(`http://localhost:8008/?ambulance=`+ ambulance, requestOptions);
        if (!response.ok){
            setErrorMessage("Patients cannot be loaded.");
        } else {
            const data = await response.json();
            setPatients(data);
            setLoaded(true);
        }
    };

    useEffect(() => {
        getMyPatients();
    }, []);

    const handleModal = () => {
        getMyPatients();
        setId(null);
    }

    return (
        <>
            <ErrorMessage message={errorMessage}/>
            {loaded && patients ? (
                <table className="table is-fullwidth">
                    <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Type</th>
                        <th>Status</th>
                        <th>Ambulance</th>
                        <th>Address</th>
                        <th>Number of people</th>
                        <th>Actions</th>
                    </tr>
                    </thead>
                    <tbody>
                    {patients.map((patient) => (
                        <tr key={patient.id}>
                            <td>{patient.id}</td>
                            <td>{patient.name}</td>
                            <td>{patient.type}</td>
                            <td>{patient.status}</td>
                            <td>{patient.ambulance}</td>
                            <td>{patient.address}</td>
                            <td>{patient.people}</td>
                            <td>
                                <button className="button mr-2 is-success is-light" onClick={()=>handleAccept(patient.id)}>Accept</button>
                                <button className="button mr-2 is-danger is-light" onClick={()=>handleReject(patient.id)}>Reject</button>
                                <button className="button mr-2 is-info is-light" onClick={()=>handleStart(patient.id)}>Start trip</button>
                                <button className="button mr-2 is-info is-light" onClick={()=>handleFinish(patient.id)}>Finish trip</button>
                            </td>
                        </tr>
                    ))}
                    </tbody>
                </table>
            ): (<p>Loading...</p>)}
        </>
    )
};

export default MyPanel;