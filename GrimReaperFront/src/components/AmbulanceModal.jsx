import React, {useEffect, useState} from 'react';

const AmbulanceModal = ({active, handleModal, token, id, setErrorMessage}) => {
    const [tag, setTag] = useState("");
    const [type, setType] = useState("");
    const [position, setPosition] = useState("");

    useEffect(() => {
        const getAmbulance = async () => {
            const requestOptions = {
                method: "GET",
                headers: {"Content-Type": "application/json"},
            };
            const response = await fetch(`http://localhost:8080/ambulances/${id}`)
            if(!response) {
                setErrorMessage("Could not retrieve ambulance data.")
            } else {
                const data = await response.json();
                setTag(data.tag);
                setType(data.type);
                setPosition(data.position);
            }
        };
        if(id){
            getAmbulance();
        }

    }, [id, token])

    const cleanFormData = () => {
    setTag("");
    setType("");
    setPosition("");
        }

    const handleCreateAmbulance = async (e) => {
        e.preventDefault();
        const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({tag: tag, type: type, position: position})
        };
        const response = await fetch("http://localhost:8080/ambulances/create", requestOptions);
        if(!response) {
            setErrorMessage("Ambulance cannot be created")
        } else {
            cleanFormData();
            handleModal();
        }
    };

    const handleUpdateAmbulance = async (e) => {
        e.preventDefault();
        const requestOptions = {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({tag: tag, type: type, position: position})
        };
        const response = await fetch(`http://localhost:8000/update/${id}`, requestOptions);
        if(!response){
            setErrorMessage("Could not update ambulance");
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
                    {id ? "Update ambulance" : "Create ambulance"}
                </h1>
            </header>
                <section className='modal-card-body'>
                    <form>
                        <div className='field'>
                            <label className='label'>Tag</label>
                            <div className="control">
                                <input
                                    type="text"
                                    placeholder="Enter ambulance tag"
                                    value={tag}
                                    onChange={(e)=>setTag(e.target.value)}
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
                                    placeholder="Enter ambulance type"
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
                                    placeholder="Enter ambulance position"
                                    value={position}
                                    onChange={(e)=>setPosition(e.target.value)}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                    </form>
                </section>
                <footer className="modal-card-foot has-background-primary-light">
                    {id ? (
                        <button className="button" onClick={handleUpdateAmbulance}>Update</button>
                    ) : (
                        <button className="button" onClick={handleCreateAmbulance}>
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

export default AmbulanceModal;