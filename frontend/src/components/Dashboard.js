import React from 'react';
import { useAuth } from '../contexts/AuthContext';

const Dashboard = () => {
  const { user, logout } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <div className="main-content">
      <div className="welcome-message">
        <h1>Welcome to your Dashboard!</h1>
        <p>You have successfully logged in.</p>
      </div>

      <div className="user-info">
        <h3>User Information</h3>
        <p><strong>Email:</strong> {user?.email}</p>
        <p><strong>User ID:</strong> {user?.id}</p>
      </div>

      <div style={{ marginTop: '2rem' }}>
        <button 
          onClick={handleLogout} 
          className="btn btn-secondary"
          style={{ marginRight: '1rem' }}
        >
          Logout
        </button>
        
        <div style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#666' }}>
          This is a protected page that can only be accessed by authenticated users.
        </div>
      </div>
    </div>
  );
};

export default Dashboard;