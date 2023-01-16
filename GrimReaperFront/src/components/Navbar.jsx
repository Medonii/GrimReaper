import React, {useState} from "react";
import '../styles/Navbar.css';

function Navbar(props) {
    const [active, setActive] = useState("nav_menu");
    const [toggleIcon, setToggleIcon] = useState("nav_toggler");
    const [role] = useState(localStorage.getItem("role"));
    //const {role} = useContext(UserContext);
    //const [roleValue, setRoleValue] = role;

        const navToggle =()=> {
            active ==='nav_menu' ? setActive('nav_menu nav_active') : setActive('nav_menu');
            toggleIcon === 'nav_toggler' ? setToggleIcon('nav_toggler toggle') : setToggleIcon('nav_toggler');
        }

    return (
        <nav className="nav">
            <ul className={active}>
                <li className="nav_item"><a href="#" className="nav_link">Home</a></li>
                {
                    role === 'Ambulance driver' || 'Admin' ? (
                            <li className="nav_item"><a href="/mypanel" className="nav_link">My panel</a></li>
                    ) : (
                        null
                    )
                }
                <li className="nav_item"><a href="/ambulances" className="nav_link">Ambulances</a></li>
                <li className="nav_item"><a href="/patients" className="nav_link">Patient requests</a></li>
                {
                    role === 'Admin' ? (
                        <li className="nav_item"><a href="/users" className="nav_link">Users</a></li>
                    ) : (
                        null
                    )
                }
            </ul>
            <div onClick={navToggle} className={toggleIcon}>
                <div className="line1"></div>
                <div className="line2"></div>
                <div className="line3"></div>
            </div>
        </nav>
    );
}

export default Navbar;