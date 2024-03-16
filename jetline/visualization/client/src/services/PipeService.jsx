// dataFetcher.js
import jsonData from '../viz-data.json';

export const fetchData = async () => {
  // Simulieren einer asynchronen Operation, z.B. das Abrufen von Daten von einer API
  const simulateAsync = new Promise((resolve) => {
    setTimeout(() => resolve(jsonData), 1000); // Verzögerung von 1 Sekunde
  });

  return simulateAsync;
};
