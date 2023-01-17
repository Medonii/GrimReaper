import React, {useEffect, useState} from 'react';

const PatientModal = ({active, handleModal, token, id, setErrorMessage}) => {
    const [name, setName] = useState("");
    const [type, setType] = useState("");
    const [address, setAddress] = useState("");
    const [noPeople, setNoPeople] = useState("");

    useEffect(() => {
        const getPatient = async () => {
            const requestOptions = {
                method: "GET",
                headers: {"Content-Type": "application/json",
                        Authorization: "Bearer " + token},
            };
            const response = await fetch(`http://localhost:8008/${id}`)
            if(!response) {
                setErrorMessage("Could not retrieve patient request data.")
            } else {
                const data = await response.json();
                setName(data.name);
                setType(data.type);
                setAddress(data.address);
                setNoPeople(data.people);
            }
        };
        if(id){
            getPatient();
        }

    }, [id, token])

    const cleanFormData = () => {
    setName("");
    setType("");
    setAddress("");
        }

    const handleCreatePatient= async (e) => {
        e.preventDefault();
        const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json",
                        Authorization: "Bearer " + token},
            body: JSON.stringify({name: name, address: address, people: noPeople, type: type})
        };
        const response = await fetch("http://localhost:8008/create", requestOptions);
        if(!response) {
            setErrorMessage("Patient cannot be created")
        } else {
            cleanFormData();
            handleModal();
        }
    };

    const handleUpdatePatient = async (e) => {
        e.preventDefault();
        const requestOptions = {
            method: "PUT",
            headers: {"Content-Type": "application/json",
                        Authorization: "Bearer " + token},
            body: JSON.stringify({name: name, address: address, people: noPeople, type: type})
        };
        const response = await fetch(`http://localhost:8008/update/${id}`, requestOptions);
        if(!response){
            setErrorMessage("Could not update patient");
        } else {
            cleanFormData();
            handleModal();
        }
    }

    return (
        <div className={`modal ${active && "is-active"}`}>
            <div className='modal-background' onClick={handleModal}></div>
            <div className='modal-card'>
            <header className='modal-card-head has-background-primary-light'>
                <h1 className='modal-card-title'>
                    {id ? "Update patient" : "Create patient"}
                </h1>
            </header>
                <section className='modal-card-body'>
                    <form>
                        <div className='field'>
                            <label className='label'>Name</label>
                            <div className="control">
                                <input
                                    type="text"
                                    placeholder="Enter patient name"
                                    value={name}
                                    onChange={(e)=>setName(e.target.value)}
                                    className="input"
                                    required
                                    />
                            </div>
                        </div>
                        <div className='field'>
                            <label className='label'>Type</label>
                            <div className="control">
                                <input
                                    type="text"
                                    placeholder="Enter patient request type"
                                    value={type}
                                    onChange={(e)=>setType(e.target.value)}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                        <div className='field'>
                            <label className='label'>Address</label>
                            <div className="control">
                                <input
                                    type="text"
                                    placeholder="Enter patient address"
                                    value={address}
                                    onChange={(e)=>setAddress(e.target.value)}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                        <div className='field'>
                            <label className='label'>No. of people</label>
                            <div className="control">
                                <input
                                    type="text"
                                    placeholder="Enter number of people"
                                    value={noPeople}
                                    onChange={(e)=>setNoPeople(e.target.value)}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                    </form>
                </section>
                <footer className="modal-card-foot has-background-primary-light">
                    {id ? (
                        <button className="button" onClick={handleUpdatePatient}>Update</button>
                    ) : (
                        <button className="button" onClick={handleCreatePatient}>
                            Create
                        </button>)
                    }
                    <button className="button" onClick={handleModal}>
                        Cancel
                    </button>

                </footer>
            </div>
        </div>

    );
};

export default PatientModal;