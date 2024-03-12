// layout/Layout.jsx
import React from 'react';
import Sidebar from '../components/layout/SidebarNav';
const Layout = ({ children }) => {
  return (
    <>
      <Sidebar />
      <div className="content" style={{ width: '100vw', height: '100vh' }}>
        {children}
      </div>
    </>
  );
};

export default Layout;
