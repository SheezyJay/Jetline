// Sidebar.jsx
import React from 'react';
import '../../assets/css/layout/sidebar.css';
import logo from '../../assets/images/logo.svg'; 

function Sidebar({ onZoomIn, onZoomOut, onFitView }) {
  return (
    <nav className="sidebar">
      <ul>
        <li>
          <a href="#" className="logo">
            <img src={logo} alt="" />
          </a>
        </li>

      </ul>
    </nav>
  );
}

export default Sidebar;
