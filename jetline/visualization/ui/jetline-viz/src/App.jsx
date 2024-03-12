// App.jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './assets/css/App.css'; 
import PipelinePage from './pages/pipeline/PipelinePage'; 
import Playground from './pages/Playground'

function App() {
  return (
   
      <Router>
        <Routes>
          <Route path="/" element={<PipelinePage />} />
          <Route path="/playground" element={<Playground />} />
        </Routes>
      </Router>
   
  );
}

export default App;
