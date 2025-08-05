import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Home = () => {
  const { isAuthenticated } = useAuth();

  return (
    <div className="main-content">
      <div className="welcome-message">
        <h1>Welcome to Auth App</h1>
        <p>A complete authentication system with React and Express</p>
      </div>

      {!isAuthenticated ? (
        <div style={{ display: 'flex', gap: '1rem', justifyContent: 'center', marginTop: '2rem' }}>
          <Link to="/login" className="btn btn-primary">
            Login
          </Link>
          <Link to="/signup" className="btn btn-secondary">
            Sign Up
          </Link>
        </div>
      ) : (
        <div style={{ marginTop: '2rem' }}>
          <p>You are already logged in!</p>
          <Link to="/dashboard" className="btn btn-primary">
            Go to Dashboard
          </Link>
        </div>
      )}

      <div style={{ marginTop: '3rem', maxWidth: '600px', margin: '3rem auto 0' }}>
        <h2>Features</h2>
        <ul style={{ textAlign: 'left', lineHeight: '1.6' }}>
          <li>✅ User registration with email and password</li>
          <li>✅ Secure password hashing with bcrypt</li>
          <li>✅ JWT token-based authentication</li>
          <li>✅ Protected routes and middleware</li>
          <li>✅ Form validation on frontend and backend</li>
          <li>✅ Persistent login state</li>
          <li>✅ Responsive design</li>
        </ul>
      </div>
    </div>
  );
};

export default Home;