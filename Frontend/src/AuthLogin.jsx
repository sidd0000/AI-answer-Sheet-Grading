
import React, { useEffect } from 'react';
import {
  BrowserRouter,
  Routes,
  Route,
  Navigate,
  useNavigate
} from 'react-router-dom';
import { Auth0Provider, useAuth0 } from '@auth0/auth0-react';

// ─── Auth0 CONFIG ────────────────────────────────────────
const domain   = 'dev-cfhm6qpdsre8l0kc.us.auth0.com';
const clientId = 'rFxT70X8BaONHtWrWV2J0JCTNqK7tUsw';
// ─────────────────────────────────────────────────────────

/** 
 * Wrap your app in Auth0Provider.
 * onRedirectCallback ensures we land back in React Router.
 */
const AuthWrapper = ({ children }) => (
  <Auth0Provider
    domain={domain}
    clientId={clientId}
    authorizationParams={{
      redirect_uri: window.location.origin,
    }}
    onRedirectCallback={(appState) => {
      // Navigate back to where we were (or default to "/")
      window.history.replaceState(
        {},
        document.title,
        appState?.returnTo || window.location.pathname
      );
    }}
  >
    {children}
  </Auth0Provider>
);

/** Landing page to choose role and trigger Auth0 login */
const Landing = () => {
  const { loginWithRedirect } = useAuth0();
  return (
    <div style={{ textAlign: 'center', marginTop: 100 }}>
      <h1>Welcome! Login as:</h1>
      <button
        onClick={() =>
          loginWithRedirect({ appState: { role: 'student' } })
        }
      >
        Student
      </button>
      <button
        style={{ marginLeft: 12 }}
        onClick={() =>
          loginWithRedirect({ appState: { role: 'teacher' } })
        }
      >
        Teacher
      </button>
    </div>
  );
};

/** Student dashboard */
const StudentDashboard = () => {
  const { user, logout } = useAuth0();
  return (
    <div style={{ textAlign: 'center', marginTop: 100 }}>
      <h2>Student Dashboard</h2>
      <p>Welcome, {user.name} ({user.email})</p>
      <button
        onClick={() =>
          logout({ logoutParams: { returnTo: window.location.origin } })
        }
      >
        Logout
      </button>
    </div>
  );
};

/** Teacher dashboard */
const TeacherDashboard = () => {
  const { user, logout } = useAuth0();
  return (
    <div style={{ textAlign: 'center', marginTop: 100 }}>
      <h2>Teacher Dashboard</h2>
      <p>Welcome, {user.name} ({user.email})</p>
      <button
        onClick={() =>
          logout({ logoutParams: { returnTo: window.location.origin } })
        }
      >
        Logout
      </button>
    </div>
  );
};

/** Main routes component */
const AppRoutes = () => {
  const { isAuthenticated, isLoading, user, appState } = useAuth0();
  const navigate = useNavigate();

  // Once Auth0 has loaded and user is authenticated, redirect based on role
  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      // 1️⃣ Prefer role from appState if you passed it
      let role = appState?.role;
      // 2️⃣ Fallback: infer from email (you can remove this)
      if (!role) {
        role = user.email.includes('teacher') ? 'teacher' : 'student';
      }
      navigate(`/${role}`, { replace: true });
    }
  }, [isLoading, isAuthenticated, user, appState, navigate]);

  if (isLoading) {
    return <div style={{ textAlign: 'center', marginTop: 100 }}>Loading…</div>;
  }

  if (!isAuthenticated) {
    return <Landing />;
  }

  // Authenticated: render dashboard routes
  return (
    <Routes>
      <Route path="/student" element={<StudentDashboard />} />
      <Route path="/teacher" element={<TeacherDashboard />} />
      {/* any other path, bounce back to the correct dashboard */}
      <Route
        path="*"
        element={
          <Navigate
            to={user.email.includes('teacher') ? '/teacher' : '/student'}
            replace
          />
        }
      />
    </Routes>
  );
};

export default function AuthLogin() {
    return (
     
        <AuthWrapper>
          <AppRoutes />
        </AuthWrapper>
      
    );
  }
