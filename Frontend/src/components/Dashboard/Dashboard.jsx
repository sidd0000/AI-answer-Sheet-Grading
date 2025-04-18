import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../../api';
import './Dashboard.css';

export default function Dashboard() {
  const [sessionId, setSessionId] = useState('');
  const [questionFile, setQuestionFile] = useState(null);
  const [markingScheme, setMarkingScheme] = useState(null);

  const [studentFile, setStudentFile] = useState(null);
  const [studentName, setStudentName] = useState('');
  const [studentId, setStudentId] = useState('');
  const [students, setStudents] = useState([]);

  const nav = useNavigate();

  // ◀ On mount, restore session & fetch students
  useEffect(() => {
    const saved = localStorage.getItem('sessionId');
    if (!saved) return;
    setSessionId(saved);

    const schemeJson = localStorage.getItem(`markingScheme_${saved}`);
    if (schemeJson) setMarkingScheme(JSON.parse(schemeJson));

    // fetch students list
    api
      .get('/get-session-results', { params: { session_id: saved } })
      .then((res) => {
        const list = res.data.students.map((s) => ({
          studentId: s.student_id,
          studentName: s.student_name,
          // parse the result string into an object
          result:
            typeof s.result === 'string'
              ? JSON.parse(s.result)
              : s.result,
        }));
        setStudents(list);
      })
      .catch(console.error);
  }, []);

  // ◀ Create a new session
  const createSession = () => {
    api
      .post('/create-session')
      .then((res) => {
        const id = res.data.session_id;
        setSessionId(id);
        localStorage.setItem('sessionId', id);
      })
      .catch(console.error);
  };

  // ◀ Delete the current session
  const deleteSession = () => {
    api
      .delete('/delete-session', { params: { session_id: sessionId } })
      .then(() => {
        localStorage.removeItem('sessionId');
        localStorage.removeItem(`markingScheme_${sessionId}`);
        setSessionId('');
        setMarkingScheme(null);
        setStudents([]);
      })
      .catch(console.error);
  };

  // ◀ Upload question paper and store scheme
  const handleQuestionUpload = async (e) => {
    e.preventDefault();
    if (!questionFile) return;
    const fd = new FormData();
    fd.append('file', questionFile);
    fd.append('session_id', sessionId);
    try {
      const res = await api.post('/upload-question-paper', fd);
      const scheme = JSON.parse(res.data.marking_scheme);
      setMarkingScheme(scheme);
      localStorage.setItem(
        `markingScheme_${sessionId}`,
        JSON.stringify(scheme)
      );
    } catch (err) {
      console.error(err);
    }
  };

  // ◀ Navigate to Marking Scheme viewer
  const viewScheme = () =>
    nav('/marking-scheme', { state: { markingScheme } });

  // ◀ Upload a student PDF and add to list
  const handleStudentUpload = async (e) => {
    e.preventDefault();
    if (!studentFile || !studentName || !studentId) return;
    const fd = new FormData();
    fd.append('file', studentFile);
    fd.append('session_id', sessionId);
    fd.append('student_name', studentName);
    fd.append('student_id', studentId);

    try {
      const res = await api.post('/upload-student-submission', fd);
      const parsed =
        typeof res.data.result === 'string'
          ? JSON.parse(res.data.result)
          : res.data.result;

      setStudents((prev) => [
        ...prev.filter((s) => s.studentId !== studentId),
        {
          studentId,
          studentName,
          result: parsed,
        },
      ]);
    } catch (err) {
      console.error(err);
    }
  };

  // ◀ Navigate to student result page, passing the student object
  const openResult = (student) =>
    nav('/student-result', { state: { student } });

  return (
    <div className="dashboard-container">
      <h1>Evaluation Dashboard</h1>

      {!sessionId ? (
        <button onClick={createSession} className="btn">
          Create New Session
        </button>
      ) : (
        <div className="session-info">
          <span>
            Session: <strong>{sessionId}</strong>
          </span>
          <button
            onClick={deleteSession}
            className="btn small-btn delete-btn"
          >
            Delete Session
          </button>
        </div>
      )}

      {sessionId && (
        <>
          <section className="upload-section">
            <h2>1. Upload Question Paper</h2>
            <form
              onSubmit={handleQuestionUpload}
              className="upload-form"
            >
              <input
                type="file"
                accept="application/pdf"
                onChange={(e) =>
                  setQuestionFile(e.target.files[0])
                }
              />
              <button type="submit" className="btn">
                Upload
              </button>
            </form>
            {markingScheme && (
              <button
                onClick={viewScheme}
                className="btn view-btn"
              >
                View Marking Scheme
              </button>
            )}
          </section>

          <section className="upload-section">
            <h2>2. Upload Student Submission</h2>
            <form
              onSubmit={handleStudentUpload}
              className="upload-form"
            >
              <input
                type="text"
                placeholder="Student Name"
                value={studentName}
                onChange={(e) =>
                  setStudentName(e.target.value)
                }
              />
              <input
                type="text"
                placeholder="Student ID"
                value={studentId}
                onChange={(e) =>
                  setStudentId(e.target.value)
                }
              />
              <input
                type="file"
                accept="application/pdf"
                onChange={(e) =>
                  setStudentFile(e.target.files[0])
                }
              />
              <button type="submit" className="btn">
                Upload
              </button>
            </form>
          </section>

          {students.length > 0 && (
            <section className="students-section">
              <h2>3. Students</h2>
              <table className="students-table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>ID</th>
                    <th>Result</th>
                  </tr>
                </thead>
                <tbody>
                  {students.map((s) => (
                    <tr key={s.studentId}>
                      <td>{s.studentName}</td>
                      <td>{s.studentId}</td>
                      <td>
                        <button
                          onClick={() => openResult(s)}
                          className="btn small-btn"
                        >
                          Open Result
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </section>
          )}
        </>
      )}
    </div>
  );
}
