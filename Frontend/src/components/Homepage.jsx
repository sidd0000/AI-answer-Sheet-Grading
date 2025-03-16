import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import "./Homepage.css";

const Homepage = () => {
  const [quote, setQuote] = useState("");

  useEffect(() => {
    const quotes = [
      "Empowering educators with AI-driven precision!",
      "Transforming assessments through automation.",
      "Grading made smarter and faster with AI.",
      "Enhancing learning through AI-powered insights.",
    ];
    setQuote(quotes[Math.floor(Math.random() * quotes.length)]);
  }, []);

  return (
    <>
      <Navbar />
      <div className="homepage">
        <header className="hero">
          <h1>AI-Powered Answer Sheet Grading</h1>
          <p>{quote}</p>
          <Link to="/signup" className="cta-button">Get Started</Link>
        </header>

        <section className="features">
          <div className="feature">
            <h2>AI-Based Grading</h2>
            <p>Utilizing NLP and AI to assess answers with precision.</p>
          </div>

          <Link to="/teacher" className="feature">
            <h2>Teacher Dashboard</h2>
            <p>Upload answer sheets, set marking schemes, and review student progress.</p>
          </Link>

          <Link to="/student" className="feature">
            <h2>Student Portal</h2>
            <p>View graded answer sheets, receive feedback, and track performance.</p>
          </Link>
        </section>

        <footer className="footer">
          <p>&copy; 2025 AI Grading System. All rights reserved.</p>
        </footer>
      </div>
    </>
  );
};

export default Homepage;
