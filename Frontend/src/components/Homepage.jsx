import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Navbar from "../components/Navbar";
import "./Homepage.css";

const Homepage = () => {
  const [quote, setQuote] = useState("");
  const [isVisible, setIsVisible] = useState({});

  useEffect(() => {
    const quotes = [
      "Empowering educators with AI-driven precision!",
      "Transforming assessments through intelligent automation.",
      "Grading reimagined: smarter, faster, more accurate.",
      "Revolutionizing education with AI-powered insights.",
    ];
    setQuote(quotes[Math.floor(Math.random() * quotes.length)]);
    
    // Intersection Observer for scroll animations
    const observerOptions = {
      threshold: 0.2,
      rootMargin: "0px 0px -50px 0px"
    };
    
    const observer = new IntersectionObserver((entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          setIsVisible(prev => ({
            ...prev,
            [entry.target.id]: true
          }));
        }
      });
    }, observerOptions);
    
    document.querySelectorAll(".observe-element").forEach(element => {
      observer.observe(element);
    });
    
    return () => observer.disconnect();
  }, []);

  return (
    <>
      <Navbar />
      <div className="homepage">
        {/* Hero */}
        <header className="cosmic_hero">
          <h1 className="cosmic_title">AI-Powered Answer Sheet Grading</h1>
          <p className="cosmic_subtitle">{quote}</p>
          <Link to="/signup" className="nova_button">Get Started</Link>
        </header>

        {/* Core Features */}
        <section className="prism_features">
          <div 
            id="feature1" 
            className={`prism_feature observe-element ${isVisible.feature1 ? 'fade-in' : ''}`}
          >
            <h2 className="prism_feature_title">AI-Based Grading</h2>
            <p className="prism_feature_text">Leveraging advanced NLP and machine learning to assess answers with human-like precision and consistency.</p>
          </div>

          <Link 
            to="/teacher" 
            id="feature2" 
            className={`prism_feature observe-element ${isVisible.feature2 ? 'fade-in' : ''}`}
          >
            <h2 className="prism_feature_title">Teacher Dashboard</h2>
            <p className="prism_feature_text">Upload answer sheets, customize marking schemes, and monitor student progress with detailed analytics.</p>
          </Link>

          <Link 
            to="/student" 
            id="feature3" 
            className={`prism_feature observe-element ${isVisible.feature3 ? 'fade-in' : ''}`}
          >
            <h2 className="prism_feature_title">Student Portal</h2>
            <p className="prism_feature_text">View graded answer sheets, receive personalized feedback, and track performance over time.</p>
          </Link>
        </section>

        {/* Extended Features */}
        <section className="prism_features nexus_features">
          <div 
            id="extFeature1" 
            className={`prism_feature observe-element ${isVisible.extFeature1 ? 'fade-in' : ''}`}
          >
            <h2 className="prism_feature_title">Multi-Language Support</h2>
            <p className="prism_feature_text">Grade answer sheets written in multiple regional and global languages with consistent accuracy.</p>
          </div>
          
          <div 
            id="extFeature2" 
            className={`prism_feature observe-element ${isVisible.extFeature2 ? 'fade-in' : ''}`}
          >
            <h2 className="prism_feature_title">Real-Time Feedback</h2>
            <p className="prism_feature_text">Instant insights for both students and teachers with detailed explanation of scoring criteria.</p>
          </div>
          
          <div 
            id="extFeature3" 
            className={`prism_feature observe-element ${isVisible.extFeature3 ? 'fade-in' : ''}`}
          >
            <h2 className="prism_feature_title">Secure & Private</h2>
            <p className="prism_feature_text">End-to-end encryption ensures data privacy with enterprise-grade security protocols.</p>
          </div>
          
          <div 
            id="extFeature4" 
            className={`prism_feature observe-element ${isVisible.extFeature4 ? 'fade-in' : ''}`}
          >
            <h2 className="prism_feature_title">Analytics & Reports</h2>
            <p className="prism_feature_text">Generate comprehensive performance summaries and trend visualization to track learning outcomes.</p>
          </div>
        </section>

        {/* Join Us Section */}
        <section 
          id="joinSection" 
          className={`aurora_section observe-element ${isVisible.joinSection ? 'fade-in' : ''}`}
        >
          <h2 className="aurora_title">Join Us in Revolutionizing Education</h2>
          <p className="aurora_text">We're on a mission to make education more efficient, equitable, and impactful through cutting-edge AI technology. Join our team of educators and engineers or collaborate with us.</p>
          <Link to="/join" className="nova_button">Join Our Mission</Link>
        </section>

        {/* Contact Form */}
        <section 
          id="contactSection" 
          className={`quantum_section observe-element ${isVisible.contactSection ? 'fade-in' : ''}`}
        >
          <h2 className="quantum_title">Contact Us</h2>
          <form className="quantum_form">
            <input type="text" placeholder="Your Name" className="quantum_input" required />
            <input type="email" placeholder="Your Email" className="quantum_input" required />
            <textarea rows="5" placeholder="Your Message" className="quantum_input quantum_textarea" required></textarea>
            <button type="submit" className="nova_button">Send Message</button>
          </form>
        </section>

        {/* Footer */}
        <footer className="orbital_footer">
          <p>&copy; 2025 AI Grading System. All rights reserved.</p>
          <p>Designed & Built by Team EdTechX</p>
          <p><a href="mailto:contact@aigrading.com" className="orbital_link">contact@aigrading.com</a></p>
        </footer>
      </div>
    </>
  );
};

export default Homepage;