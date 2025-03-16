import React, { useState, useEffect } from 'react';
import './TeacherDashboard.css';

function TeacherDashboard() {
  const [activeTab, setActiveTab] = useState('upload');
  const [markingScheme, setMarkingScheme] = useState(null);
  const [studentAnswerSheets, setStudentAnswerSheets] = useState([]);
  const [numStudents, setNumStudents] = useState('');
  const [uploadStatus, setUploadStatus] = useState('');

  useEffect(() => {
    document.title = 'Teacher Dashboard';
    return () => {
      document.title = 'React App';
    };
  }, []);

  useEffect(() => {
    if (studentAnswerSheets.length > 0 || markingScheme) {
      setUploadStatus('Files selected for upload');
    } else {
      setUploadStatus('');
    }
  }, [studentAnswerSheets, markingScheme]);

  const handleMarkingSchemeUpload = (event) => {
    setMarkingScheme(event.target.files[0]);
  };

  const handleStudentSheetsUpload = (event) => {
    setStudentAnswerSheets([...event.target.files]);
  };

  const handleNumStudentsChange = (event) => {
    setNumStudents(event.target.value);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    console.log("Marking scheme:", markingScheme);
    console.log("Student Answer Sheets:", studentAnswerSheets);
    console.log("Number of students:", numStudents);
    setUploadStatus('Uploading...');
    // Simulate API call delay
    setTimeout(() => {
      setUploadStatus('Upload completed!');
    }, 2000);
  };

  const renderUploadPage = () => (
    <div className="upload-page">
      <h2>Upload Files</h2>
      <form onSubmit={handleSubmit} className="upload-form">
        <div className="form-group">
          <label htmlFor="markingScheme" style={{color:'black'}}>
            Upload Marking Scheme / Answers (PDF):
          </label>
          <input
            type="file"
            id="markingScheme"
            accept=".pdf"
            onChange={handleMarkingSchemeUpload}
          />
        </div>
        <div className="form-group">
          <label htmlFor="studentSheets" style={{color:'black'}}>
            Upload Student Answer Sheets (PDFs):
          </label>
          <input
            type="file"
            id="studentSheets"
            accept=".pdf"
            multiple
            onChange={handleStudentSheetsUpload}
          />
        </div>
        <div className="form-group">
          <label htmlFor="numStudents" style={{color:'black'}}>Number of Students:</label>
          <input
            type="number"
            id="numStudents"
            min="1"
            value={numStudents}
            onChange={handleNumStudentsChange}
            placeholder="Enter number of students"
          />
        </div>
        <button type="submit">Upload Files</button>
        {uploadStatus && <p className="upload-status">{uploadStatus}</p>}
      </form>
    </div>
  );

  const renderAnalyticsPage = () => (
    <div className="analytics-page">
      <h2>Upload Summary</h2>
      <div className="analytics-card">
        <h3>Marking Scheme</h3>
        {markingScheme ? (
          <ul>
            <li>
              <strong>Name:</strong> {markingScheme.name}
            </li>
            <li>
              <strong>Size:</strong> {(markingScheme.size / 1024).toFixed(2)} KB
            </li>
            <li>
              <strong>Type:</strong> {markingScheme.type}
            </li>
          </ul>
        ) : (
          <p>No marking scheme uploaded.</p>
        )}
      </div>
      <div className="analytics-card">
        <h3>Student Answer Sheets</h3>
        {studentAnswerSheets.length > 0 ? (
          <ul>
            {studentAnswerSheets.map((file, index) => (
              <li key={index}>
                {file.name} - {(file.size / 1024).toFixed(2)} KB
              </li>
            ))}
          </ul>
        ) : (
          <p>No student answer sheets uploaded.</p>
        )}
      </div>
      <div className="analytics-card">
        <h3>Class Information</h3>
        <p>
          <strong>Number of Students:</strong>{' '}
          {numStudents ? numStudents : 'Not specified'}
        </p>
      </div>
    </div>
  );

  return (
    <div className="teacher-dashboard">
      <header className="dashboard-header">
        <h1>Teacher Dashboard</h1>
        <nav className="dashboard-nav">
          <button
            className={activeTab === 'upload' ? 'active' : ''}
            onClick={() => setActiveTab('upload')}
          >
            Upload Files
          </button>
          <button
            className={activeTab === 'analytics' ? 'active' : ''}
            onClick={() => setActiveTab('analytics')}
          >
            Upload Summary
          </button>
        </nav>
      </header>
      <main className="dashboard-content">
        {activeTab === 'upload' ? renderUploadPage() : renderAnalyticsPage()}
      </main>
      <footer className="dashboard-footer">
        <p>
          &copy; {new Date().getFullYear()} Teacher Dashboard. All rights reserved.
        </p>
      </footer>
    </div>
  );
}

export default TeacherDashboard;
