import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';


import { Home } from './pages/Home.jsx';
import { Alerts } from './pages/Alerts.tsx';
import { EquipmentDetails } from './pages/EquipmentDetails.jsx';
import { Navbar } from './components/Navbar.tsx';


function App() {
  return (
    <Router>
      <div className="app">
        <Navbar />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/equipment/:id" element={<EquipmentDetails />} />
            <Route path="/alerts" element={<Alerts />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;