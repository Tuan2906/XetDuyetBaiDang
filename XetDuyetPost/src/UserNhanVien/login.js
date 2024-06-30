import React, { useState } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import APIs, { endpoints } from '../configs/APIs';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faUser, faLock } from '@fortawesome/free-solid-svg-icons';
const Login = ({ setIsLoggedIn, setUser, user }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [err, setErr] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const formData = new FormData();
      formData.append('username', username);
      formData.append('password', password);
      console.log("F",username);
      // Perform login API call
      let res = await APIs.post(endpoints["login"], formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });

      console.log(res.data.access_token);
     localStorage.setItem("access-token", res.data.access_token)
      console.log("acces token",localStorage.getItem("access-token"));
      const {user}=res.data;
      setIsLoggedIn(true);
      setUser(user);
      setErr(false);

      // Redirect user to the previous page or '/journeys'
      const from = location.state?.from?.pathname || '/journeys';
      navigate(from, { replace: true });
    } catch (ex) {
      console.error('Login error:', ex);
      setErr(true);
    }
  };

  return (
    <div className="container d-flex justify-content-center align-items-center" style={{ minHeight: '100vh' }}>
      <div className="card p-4 shadow" style={{ maxWidth: '400px', width: '100%' }}>
        <h2 className="mb-4">Login</h2>
        {err && <div className="alert alert-danger">Invalid credentials. Please try again.</div>}
        <form onSubmit={handleSubmit}>
          <div className="mb-3">
            <label htmlFor="username" className="form-label visually-hidden">Username</label>
            <div className="input-group">
              <span className="input-group-text"><FontAwesomeIcon icon={faUser} /></span>
              <input
                type="text"
                className="form-control"
                id="username"
                placeholder="Username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
              />
            </div>
          </div>
          <div className="mb-3">
            <label htmlFor="password" className="form-label visually-hidden">Password</label>
            <div className="input-group">
              <span className="input-group-text"><FontAwesomeIcon icon={faLock} /></span>
              <input
                type="password"
                className="form-control"
                id="password"
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
              />
            </div>
          </div>
          <div className="mb-10">
            <button type="submit" className="btn btn-primary d-block mx-auto" style={{margin:"20px"}}>Login</button>
            <p className="mt-100-alert alert-danger">Ghi Chú: Chỉ có nhân viên được phép đăng nhập.</p>

          </div>

        </form>
      </div>
    </div>
  );
};

export default Login;
