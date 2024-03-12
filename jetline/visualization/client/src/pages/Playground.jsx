import React, { useState } from 'react';
import InfoSidebar from '../components/content/InfoSidebar';
import PipelineDataFetcher from '../services/PipeService'; // Stellen Sie sicher, dass der Pfad korrekt ist

function PipelinePage() {
    const [isOpen, setIsOpen] = useState(false);
  const [data, setData] = useState({
    name: '',
    links: []
  });

  const toggleSidebar = (sidebarData) => {
    setData(sidebarData);
    setIsOpen(!isOpen);
  };
  const closeSidebar = () => {
    setIsOpen(false);
  };
  

  return (
    <div>
      <h1>Pipeline-Seite</h1>
     

      <button onClick={() => toggleSidebar({ name: 'Max Mustermann', links: ['Link 1', 'Link 2', 'Link 3', 'Link 4'] })}>
        {isOpen ? 'Close Sidebar' : 'Open Sidebar'}
      </button>
    
     
      <InfoSidebar isOpen={isOpen} data={data} onClose={closeSidebar} />
      <PipelineDataFetcher />
    </div>
  );
}

export default PipelinePage;
