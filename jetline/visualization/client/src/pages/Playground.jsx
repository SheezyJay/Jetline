import React, { useState, useEffect } from 'react';

import { fetchData } from '../services/PipeService';



function PipelinePage() {
  const [data, setData] = useState(null);

  useEffect(() => {
    fetchData().then(data => {
      setData(data);
    });
  }, []);

  return (
    <div>
      {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : <p>Daten werden geladen...</p>}
    </div>
  );
}
export default PipelinePage;
