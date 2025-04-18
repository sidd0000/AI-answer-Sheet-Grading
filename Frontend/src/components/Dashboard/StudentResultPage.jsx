import React, { useEffect } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './StudentResultPage.css';

export default function StudentResultPage() {
  const { state } = useLocation();
  const { student } = state || {};
  const nav = useNavigate();

  // debug
  useEffect(() => {
    if (student) console.log('▶ student.result', student.result);
  }, [student]);

  // no student at all
  if (!student) {
    return (
      <div className="result-container">
        <button onClick={() => nav(-1)} className="btn back-btn">
          ← Back
        </button>
        <p style={{ textAlign: 'center', marginTop: '2rem' }}>
          No student data available.
        </p>
      </div>
    );
  }

  const { studentName, studentId, result } = student;

  // guard empty result object
  if (
    !result ||
    typeof result !== 'object' ||
    Object.keys(result).length === 0
  ) {
    return (
      <div className="result-container">
        <button onClick={() => nav(-1)} className="btn back-btn">
          ← Back
        </button>
        <h1 style={{ textAlign: 'center', marginTop: '1rem' }}>
          {studentName} ({studentId})
        </h1>
        <p style={{ textAlign: 'center', marginTop: '2rem' }}>
          No detailed result found for this student.
        </p>
      </div>
    );
  }

  return (
    <div className="result-container">
      <button onClick={() => nav(-1)} className="btn back-btn">
        ← Back
      </button>
      <h1>
        {studentName} ({studentId}) — Evaluation Report
      </h1>

      {Object.entries(result).map(([question, info]) => (
        <div key={question} className="question-block">
          <h2>
            {question} — Total Awarded: {info.total_awarded}
          </h2>

          {info.steps && info.steps.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>Step</th>
                  <th>Expected Marks</th>
                  <th>Awarded Marks</th>
                </tr>
              </thead>
              <tbody>
                {info.steps.map((step, idx) => (
                  <tr key={idx}>
                    <td>{step.keyword}</td>
                    <td>{step.expected_marks}</td>
                    <td
                      className={
                        step.awarded_marks > 0
                          ? 'awarded'
                          : 'not-awarded'
                      }
                    >
                      {step.awarded_marks}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <h3>Not attempted</h3>
          )}
        </div>
      ))}
    </div>
  );
}
