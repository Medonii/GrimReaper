import React, {useContext, useState, useEffect} from 'react';
import ErrorMessage from "./ErrorMessage";
import {UserContext} from "../context/UserContext";
import UserModal from "./UserModal";

const Users = () => {
    const [token] = useContext(UserContext);
    const [user,setUser] = useState(null);
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
            headers: {"Content-Type": "application/json"},
        };
        const response = await fetch(`http://localhost:8080/users/delete_user/${id}`, requestOptions);
        if(!response.ok) {
            setErrorMessage("Failed to delete user")
        } else {
            getUsers();
        }
    }

    const getUsers = async() => {
        const requestOptions = {
            method: "GET",
            headers: {"Content-Type": "application/json"},
        };
        const response = await fetch("http://localhost:8080/users", requestOptions);
        if (!response.ok){
            setErrorMessage("Users cannot be loaded.");
        } else {
            const data = await response.json();
            setUser(data);
            setLoaded(true);
        }
    };

    useEffect(() => {
        getUsers();
    }, []);

    const handleModal = () => {
        setActiveModal(!activeModal);
        getUsers();
        setId(null);
    }

    return (
        <>
            <UserModal active={activeModal} handleModal={handleModal} token={token} id={id} setErrorMessage={setErrorMessage}/>
            <button className="button mb-5 is-primary" onClick={() => setActiveModal(true)}>
                Add a new user
            </button>
            <ErrorMessage message={errorMessage}/>
            {loaded && user ? (
                <table className="table is-fullwidth">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nickname</th>
                            <th>Role</th>
                            <th>Ambulance</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                            {user.map((user) => (
                                <tr key={user.id}>
                                <td>{user.id}</td>
                                <td>{user.nickname}</td>
                                <td>{user.role}</td>
                                <td>{user.ambulance}</td>
                                    <td>
                                        <button className="button mr-2 is-info is-light" onClick={()=>handleUpdate(user.id)}>Update</button>
                                        <button className="button mr-2 is-danger is-light" onClick={()=>handleDelete(user.id)}>Delete</button>
                                    </td>
                                </tr>
                                ))}
                    </tbody>
                </table>
            ): (<p>Loading...</p>)}
        </>
    )
};

export default Users;