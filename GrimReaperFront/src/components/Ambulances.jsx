import React, {useContext, useState, useEffect} from 'react';
import ErrorMessage from "./ErrorMessage";
import {UserContext} from "../context/UserContext";
import AmbulanceModal from "./AmbulanceModal";

const Ambulances = () => {
    const [token] = useContext(UserContext);
    const [ambulances,setAmbulances] = useState(null);
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
        const response = await fetch(`http://api-gateway-service:8080/ambulances/delete_ambulance/${id}`, requestOptions);
        if(!response.ok) {
            setErrorMessage("Failed to delete ambulance")
        } else {
            getAmbulances();
        }
    }

    const getAmbulances = async() => {
        const requestOptions = {
            method: "GET",
            headers: {"Content-Type": "application/json",
                        Authorization: "Bearer " + token},
        };
        const response = await fetch("http://ambulance-service:8000/", requestOptions);
        if (!response.ok){
            setErrorMessage("Ambulances cannot be loaded.");
        } else {
            const data = await response.json();
            setAmbulances(data);
            setLoaded(true);
        }
    };

    useEffect(() => {
        getAmbulances();
    }, []);

    const handleModal = () => {
        setActiveModal(!activeModal);
        getAmbulances();
        setId(null);
    }

    return (
        <>
            <AmbulanceModal active={activeModal} handleModal={handleModal} token={token} id={id} setErrorMessage={setErrorMessage}/>
            <button className="button mb-5 is-primary" onClick={() => setActiveModal(true)}>
                Add a new ambulance
            </button>
            <ErrorMessage message={errorMessage}/>
            {loaded && ambulances ? (
                <table className="table is-fullwidth">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Tag</th>
                            <th>Type</th>
                            <th>Status</th>
                            <th>Position</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                            {ambulances.map((ambulance) => (
                                <tr key={ambulance.id}>
                                <td>{ambulance.id}</td>
                                <td>{ambulance.tag}</td>
                                <td>{ambulance.type}</td>
                                <td>{ambulance.status}</td>
                                <td>{ambulance.position}</td>
                                    <td>
                                        <button className="button mr-2 is-info is-light" onClick={()=>handleUpdate(ambulance.id)}>Update</button>
                                        <button className="button mr-2 is-danger is-light" onClick={()=>handleDelete(ambulance.id)}>Delete</button>
                                    </td>
                                </tr>
                                ))}
                    </tbody>
                </table>
            ): (<p>Loading...</p>)}
        </>
    )
};

export default Ambulances;