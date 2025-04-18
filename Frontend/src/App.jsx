import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Homepage from "./components/Homepage";
import Navbar from "./components/Navbar";
import Dashboard from './components/Dashboard/Dashboard';
import MarkingSchemePage from './components/Dashboard/MarkingSchemePage';
import StudentResultPage from './components/Dashboard/StudentResultPage'
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/teacher" element={<Dashboard />} />
        <Route path="/" element={<Homepage />} />
        <Route path="/marking-scheme" element={<MarkingSchemePage />} />
        <Route path="/student-result" element={<StudentResultPage />} />
      </Routes>
    </Router>
  );
}

export default App;
