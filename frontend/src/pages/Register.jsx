import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Register = () => {
  const [name, setName] = useState("");
  const [role, setRole] = useState("employee");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleRegister = (e) => {
    e.preventDefault();
    if (!name || !role || !email || !password) {
      alert("All fields are required!");
      return;
    }
    alert("User registered successfully!");
  };

  return (
    <div className="container">
      <div className="card">
        <div className="toggle-buttons">
          <button onClick={() => navigate("/login")}>Login</button>
          <button className="active">Register</button>
        </div>
        
        <form onSubmit={handleRegister}>
          <label>Name</label>
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
          <label>Role</label>
          <select value={role} onChange={(e) => setRole(e.target.value)} required>
            <option value="employee">Employee</option>
            <option value="manager">Manager</option>
          </select>
          <label>Email</label>
          <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} required />
          <label>Password</label>
          <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} required />
          <button type="submit" className="submit-btn">Register</button>
        </form>
      </div>
    </div>
  );
};

export default Register;
