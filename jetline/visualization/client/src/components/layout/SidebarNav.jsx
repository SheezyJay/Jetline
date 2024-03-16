import React from "react";
import "../../assets/css/layout/sidebar.css";
import RocketIcon from '@mui/icons-material/Rocket';


function Sidebar({}) {
 

 

  return (
    <nav className="sidebar">
      <ul>
        <li>
          <a href="https://kdc-solutions.de/" target="_blank" className="logo">
            <RocketIcon style={{ fontSize: 30, color: 'var(--primary-color)' }} />
          </a>
        </li>
       
      </ul>
    </nav>
  );
}

export default Sidebar;
