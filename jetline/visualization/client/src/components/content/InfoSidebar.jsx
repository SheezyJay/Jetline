import React, { useRef, useEffect, useState } from "react";
import "./InfoSidebar.css";
import CloseIcon from "@mui/icons-material/Close";
import VisibilityIcon from "@mui/icons-material/Visibility"; // Importieren Sie das Auge-Icon
import Prism from "prismjs";
import "./codeThemeDefault.css";
import "prismjs/components/prism-python";

const InfoSidebar = ({ isOpen, data, onClose, onToggle }) => {
  const [showCodeSidebar, setShowCodeSidebar] = useState(false); // Zustand für die Anzeige der Code-Sidebar
  const sidebarRef = useRef(null);
  const codeSidebarRef = useRef(null);
  const closeButtonRef = useRef(null);
  const codeRef = useRef(null); // Referenz für den Code-Container

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (
        sidebarRef.current &&
        !sidebarRef.current.contains(event.target) &&
        (!codeSidebarRef.current ||
          !codeSidebarRef.current.contains(event.target)) // Prüft, ob der Klick außerhalb der Code-Sidebar erfolgte
      ) {
        onClose(); // Schließt die Haupt-Sidebar
        setShowCodeSidebar(false); // Schließt die Code-Sidebar
      }
    };

    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    } else {
      document.removeEventListener("mousedown", handleClickOutside);
    }

    // Initialisieren Sie Prism.js nach dem Rendern der Komponente
    Prism.highlightAll();

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen, onClose, codeRef, setShowCodeSidebar]);

  useEffect(() => {
    if (showCodeSidebar) {
      Prism.highlightAll();
    }
  }, [showCodeSidebar, data.code]);

  const handleCloseButtonClick = () => {
    onClose();
    if (showCodeSidebar) {
      setShowCodeSidebar(false);
    }
  };

  const handleEyeClick = () => {
    if (showCodeSidebar) {
      setShowCodeSidebar(false);
    } else {
      setShowCodeSidebar(true);
    }
  };

  return (
    <div className="sidebar-wrapper">
      <div ref={sidebarRef} className={`info-sidebar ${isOpen ? "open" : ""}`}>
        <div id="popup" className="popup">
          <div className="sidebar-header">
            <h2 className="component-title">
              {/* icon */}
              <span className="component-title-span" data-attr="title">
                Title
              </span>
            </h2>
            <div className="icons-container">
              {data.code && (
                <span
                  className="eye-icon"
                  style={{
                    marginRight: "10px",
                    fontSize: 16,
                    cursor: "pointer",
                  }}
                  onClick={handleEyeClick}
                >
                  <VisibilityIcon />
                </span>
              )}
              <button
                ref={closeButtonRef}
                className="close-btn"
                onClick={handleCloseButtonClick}
              >
                <CloseIcon />
              </button>
            </div>
          </div>
          <div>
            <div className="right-content-box">
              <h3 className="label">Original Node Name:</h3>
              <p className="label-content">
                {data.title ? data.title : "-----"}
              </p>
            </div>
            <div className="right-content-box">
              <h3 className="label">Description:</h3>
              <p className="label-content">
                {data.description ? data.description : "-----"}
              </p>
            </div>
            <div className="right-content-box">
              <h3 className="label">Type:</h3>
              <p className="label-content">
                {data.type ? data.type : "-----"}
              </p>
            </div>
            
            

              <div className="right-content-box">
                <h3 className="label">Input:</h3>
                <p className="label-content">{data.inputs ? data.inputs : "-----"}</p>
              </div>
              <div className="right-content-box">
                <h3 className="label">Output:</h3>
                <p className="label-content">{data.outputs ? data.outputs : "-----"}</p>
              </div>
         
          </div>
        </div>
      </div>

      {showCodeSidebar && (
        <div ref={codeSidebarRef} className="code-sidebar">
          <div className="code-sidebar-header">
            <h2>Source Code:</h2>
          </div>
          <div className="code-content">
            <pre style={{ backgroundColor: "var(--secondary-background)" }}>
              <code className="language-python">{data.code}</code>
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};

export default InfoSidebar;
