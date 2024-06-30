import React, { useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import './App.css';
import Login from './UserNhanVien/login';
import JourneyTable from './XetDuyetBaiDang/JourneyTable';


const App = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login setIsLoggedIn={setIsLoggedIn} setUser={setUser} user={user} />} />
        <Route path="/journeys" element={
          <PrivateRoute isLoggedIn={isLoggedIn} user={user}>
            <JourneyTable />
          </PrivateRoute>
        } />
        <Route path="/" element={<Navigate to="/login" />} />
      </Routes>
    </Router>
  );
};

const PrivateRoute = ({ children, isLoggedIn, user }) => {
  if (!isLoggedIn) {
    return <Navigate to="/login" />;
  }
  return React.cloneElement(children, { user });
};

export default App;
