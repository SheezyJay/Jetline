import React, { useState } from 'react';
import Sidebar from '../components/layout/SidebarNav';

function Layout({ children }) {
  const [isRunning, setIsRunning] = useState(false);

  const handleStart = () => {
   
    setIsRunning(true);
    // Hier können Sie zusätzliche Logik zum Starten der Pipeline einfügen
  };

  const handleStop = () => {
    setIsRunning(false);
    // Hier können Sie zusätzliche Logik zum Stoppen der Pipeline einfügen
  };

  return (
    <>
      <Sidebar onStart={handleStart} onStop={handleStop} isRunning={isRunning} />
      <div className="content" style={{ width: '100vw', height: '100vh' }}>
        {children}
      </div>
    </>
  );
}

export default Layout;
