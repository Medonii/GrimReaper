import React, {useContext, useState, useEffect} from 'react';
import ErrorMessage from "./ErrorMessage";
import {UserContext} from "../context/UserContext";
import PatientModal from "./PatientModal";

const Patients = () => {
    const [token] = useContext(UserContext);
    const [patients,setPatients] = useState(null);
    const [errorMessage, setErrorMessage] = useState("");
    const [loaded, setLoaded] = useState(false);
    const [activeModal, setActiveModal] = useState(false);
    const [id, setId] = useState(null);

    const handleUpdate = async (id) => {
        setId(id);
        setActiveModal(true);
    };

    const handleDelete = async (id) => {
        const requestOptions = {
            method: "DELETE",
            headers: {"Content-Type": "application/json",
                        Authorization: "Bearer " + token},
        };
        const response = await fetch(`http://localhost:8080/patients/delete/${id}`, requestOptions);
        if(!response.ok) {
            setErrorMessage("Failed to delete patient")
        } else {
            getPatients();
        }
    }

    const handleSuggest = async (id) => {
        const requestOptions = {
            method: "PUT",
            headers: {"Content-Type": "application/json",
                        Authorization: "Bearer " + token},
        };
        const response = await fetch(`http://localhost:8008/suggest/${id}`, requestOptions);
        if(!response.ok) {
            setErrorMessage("Failed to assign ambulance")
        } else {
            getPatients();
        }
    }

    const getPatients = async() => {
        const requestOptions = {
            method: "GET",
            headers: {"Content-Type": "application/json",
                        Authorization: "Bearer " + token},
        };
        const response = await fetch("http://localhost:8080/patients", requestOptions);
        if (!response.ok){
            setErrorMessage("Patients cannot be loaded.");
        } else {
            const data = await response.json();
            setPatients(data);
            setLoaded(true);
        }
    };

    useEffect(() => {
        getPatients();
    }, []);

    const handleModal = () => {
        setActiveModal(!activeModal);
        getPatients();
        setId(null);
    }

    return (
        <>
            <PatientModal active={activeModal} handleModal={handleModal} token={token} id={id} setErrorMessage={setErrorMessage}/>
            <button className="button mb-5 is-primary" onClick={() => setActiveModal(true)}>
                Add a new patient
            </button>
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
                                        <button className="button mr-2 is-info is-light" onClick={()=>handleUpdate(patient.id)}>Update</button>
                                        <button className="button mr-2 is-danger is-light" onClick={()=>handleDelete(patient.id)}>Delete</button>
                                        <button className="button mr-2 is-success is-light" onClick={()=>handleSuggest(patient.id)}>Assign ambulance</button>
                                    </td>
                                </tr>
                                ))}
                    </tbody>
                </table>
            ): (<p>Loading...</p>)}
        </>
    )
};

export default Patients;