import React, { useState, useEffect } from 'react';
import jsonData from '../viz-data.json';

function PipelineDataFetcher() {
  const [pipelineData, setPipelineData] = useState(null);

  useEffect(() => {
    const storedData = localStorage.getItem('pipelineData');
    if (storedData) {
      setPipelineData(JSON.parse(storedData));
    } else {
      // Wenn keine gespeicherten Daten vorhanden sind, setzen Sie die Daten auf jsonData
      setPipelineData(jsonData);
      // Speichern der Daten im lokalen Speicher
      localStorage.setItem('pipelineData', JSON.stringify(jsonData));
    }
  }, []);

  return (
    <div>
      {pipelineData ? (
        <div>
          <h2>Pipeline Data</h2>
          <pre>{JSON.stringify(pipelineData, null, 2)}</pre>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

export default PipelineDataFetcher;
