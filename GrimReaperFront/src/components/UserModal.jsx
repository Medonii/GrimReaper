import React, {useEffect, useState} from 'react';

const UserModal = ({active, handleModal, token, id, setErrorMessage}) => {
    const [nickname, setNickname] = useState("");
    const [password, setPassword] = useState("");
    const [role, setRole] = useState("");
    const [ambulance, setAmbulance] = useState("");

    useEffect(() => {
        const getUsers = async () => {
            const requestOptions = {
                method: "GET",
                headers: {"Content-Type": "application/json"},
            };
            const response = await fetch(`http://localhost:8080/users/${id}`, requestOptions)
            if(!response) {
                setErrorMessage("Could not retrieve user data.")
            } else {
                const data = await response.json();
                setNickname(data.nickname);
                setPassword(data.password);
                setRole(data.role);
                setAmbulance(data.ambulance)
            }
        };
        if(id){
            getUsers();
        }

    }, [id, token])

    const cleanFormData = () => {
    setNickname("");
    setPassword("");
    setRole("");
        }

    const handleCreateUser = async (e) => {
        e.preventDefault();
        const requestOptions = {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({nickname: nickname, password: password, role: role, ambulance: ambulance})
        };
        const response = await fetch("http://localhost:8080/users/create", requestOptions);
        if(!response) {
            setErrorMessage("User cannot be created")
        } else {
            cleanFormData();
            handleModal();
        }
    };

    const handleUpdateUser = async (e) => {
        e.preventDefault();
        const requestOptions = {
            method: "PUT",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({nickname: nickname, password: password, role: role, ambulance: ambulance})
        };
        const response = await fetch(`http://localhost:8080/users/update_user/${id}`, requestOptions);
        if(!response){
            setErrorMessage("Could not update user");
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
                    {id ? "Update user" : "Create user"}
                </h1>
            </header>
                <section className='modal-card-body'>
                    <form>
                        <div className='field'>
                            <label className='label'>Nickname</label>
                            <div className="control">
                                <input
                                    type="text"
                                    placeholder="Enter ambulance nickname"
                                    value={nickname}
                                    onChange={(e)=>setNickname(e.target.value)}
                                    className="input"
                                    required
                                    />
                            </div>
                        </div>
                        <div className='field'>
                            <label className='label'>Password</label>
                            <div className="control">
                                <input
                                    type="password"
                                    placeholder="Enter user password"
                                    value={password}
                                    onChange={(e)=>setPassword(e.target.value)}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                        <div className='field'>
                            <label className='label'>Role</label>
                            <div className="control">
                                <input
                                    type="text"
                                    placeholder="Enter role"
                                    value={role}
                                    onChange={(e)=>setRole(e.target.value)}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                        <div className='field'>
                            <label className='label'>Ambulance</label>
                            <div className="control">
                                <input
                                    type="text"
                                    placeholder="Enter ambulance tag"
                                    value={ambulance}
                                    onChange={(e)=>setAmbulance(e.target.value)}
                                    className="input"
                                    required
                                />
                            </div>
                        </div>
                    </form>
                </section>
                <footer className="modal-card-foot has-background-primary-light">
                    {id ? (
                        <button className="button" onClick={handleUpdateUser}>Update</button>
                    ) : (
                        <button className="button" onClick={handleCreateUser}>
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

export default UserModal;