import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Homepage from "./components/Homepage";
import TeacherDashboard from "./pages/TeacherDashboard/TeacherDashboard";
import Navbar from "./components/Navbar";
import StudentDashboard from "./pages/StudentDashboard/StudentDashboard";
function App() {
  return (
    <Router>
        
      <Routes>
        <Route path="/" element={<Homepage />} />
        <Route path="/teacher" element={<TeacherDashboard />} />   
        <Route path="/student" element={<StudentDashboard />} />   

      </Routes>
    </Router>
  );
}

export default App;
