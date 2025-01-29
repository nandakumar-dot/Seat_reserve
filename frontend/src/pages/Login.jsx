import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    if (!email || !password) {
      alert("Please fill in both fields!");
      return;
    }
    if (email === "test@example.com" && password === "password") {
      alert("Login successful!");
      navigate("/dashboard");
    } else {
      alert("Invalid email or password!");
    }
  };

  return (
    <div className="container">
      <div className="card">
        <div className="toggle-buttons">
          <button className="active">Login</button>
          <button onClick={() => navigate("/register")}>Register</button>
        </div>
        
        <form onSubmit={handleLogin}>
          <label>Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <label>Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          <button type="submit" className="submit-btn">Login</button>
        </form>
      </div>
    </div>
  );
};

export default Login;
