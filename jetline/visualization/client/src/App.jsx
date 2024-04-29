// App.jsx
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import './assets/css/App.css'; 
import PipelinePage from './pages/pipeline/PipelinePage';

function App() {
  return (
   
      <Router>
        <Routes>
          <Route path="/" element={<PipelinePage />} />
        </Routes>
      </Router>
   
  );
}

export default App;
