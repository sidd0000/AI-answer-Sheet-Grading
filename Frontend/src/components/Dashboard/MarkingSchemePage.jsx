// src/components/MarkingSchemePage.jsx
import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import './MarkingSchemePage.css';

export default function MarkingSchemePage() {
  const { state } = useLocation();
  const { markingScheme } = state || {};
  const nav = useNavigate();

  if (!markingScheme) {
    return <p style={{ textAlign: 'center' }}>No marking scheme data available.</p>;
  }

  return (
    <div className="scheme-container">
      <button onClick={() => nav(-1)} className="btn back-btn">← Back</button>
      <h1>Marking Scheme</h1>

      {Object.entries(markingScheme).map(([question, info]) => (
        <div key={question} className="question-block">
          {/* use total_marks not total_expected */}
          <h2>{question} — Total Marks: {info.total_marks}</h2>

          {info.steps && info.steps.length > 0 ? (
            <table>
              <thead>
                <tr>
                  <th>Step</th>
                  {/* rename header to reflect ‘marks’ */}
                  <th>Marks</th>
                </tr>
              </thead>
              <tbody>
                {info.steps.map((step, i) => (
                  <tr key={i}>
                    <td>{step.keyword}</td>
                    {/* use step.marks not expected_marks */}
                    <td>{step.marks}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          ) : (
            <h3>No steps defined</h3>
          )}
        </div>
      ))}
    </div>
  );
}
