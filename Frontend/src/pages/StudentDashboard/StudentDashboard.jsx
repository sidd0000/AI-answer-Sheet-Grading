import React from 'react';
import  './StudentDashboard.css';

// Dummy data for demonstration
const dummyData = [
  {
    id: 1,
    fileName: "AnswerSheet1.pdf",
    result: "85%",
    feedback: "Good job, but please review question 3 for improvement.",
  },
  {
    id: 2,
    fileName: "AnswerSheet2.pdf",
    result: "92%",
    feedback: "Excellent work overall!",
  },
];

function StudentDashboard() {
  return (
    <div className="student-dashboard">
      <h1>Student Dashboard</h1>
      <div className="answer-sheets">
        {dummyData.map((sheet) => (
          <div key={sheet.id} className="answer-sheet">
            <h3>{sheet.fileName}</h3>
            <p><strong>Result:</strong> {sheet.result}</p>
            <p><strong>Feedback:</strong> {sheet.feedback}</p>
            <a href="#" className="view-pdf">
              View PDF
            </a>
          </div>
        ))}
      </div>
    </div>
  );
}

export default StudentDashboard;
