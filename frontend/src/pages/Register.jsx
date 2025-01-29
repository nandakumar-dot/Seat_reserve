import { useState } from "react";

const Register = () => {
  const [name, setName] = useState("");
  const [role, setRole] = useState("employee"); // Default role
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState("");

  const handleRegister = (e) => {
    e.preventDefault();

    if (!name || !role || !email || !password) {
      setErrorMessage("All fields are required!");
      return;
    }

    setErrorMessage(""); // Clear error message if validation passes

    // Simulate user registration
    const newUser = { name, role, email, password };
    console.log("Registered User:", newUser);

    // Save to localStorage (not secure for real apps)
    localStorage.setItem("user", JSON.stringify(newUser));

    alert("User registered successfully!");

    // Clear input fields
    setName("");
    setRole("employee");
    setEmail("");
    setPassword("");
  };

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", marginTop: "50px" }}>
      <h1>Register</h1>
      <form onSubmit={handleRegister} style={{ display: "flex", flexDirection: "column", width: "80%", maxWidth: "300px" }}>
        <label>Name:</label>
        <input
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          required
          style={{ marginBottom: "10px", padding: "10px", fontSize: "16px" }}
        />

        <label>Role:</label>
        <select
          value={role}
          onChange={(e) => setRole(e.target.value)}
          required
          style={{ marginBottom: "10px", padding: "10px", fontSize: "16px" }}
        >
          <option value="employee">Employee</option>
          <option value="manager">Manager</option>
        </select>

        <label>Email:</label>
        <input
          type="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{ marginBottom: "10px", padding: "10px", fontSize: "16px" }}
        />

        <label>Password:</label>
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ marginBottom: "20px", padding: "10px", fontSize: "16px" }}
        />

        {errorMessage && <p style={{ color: "red" }}>{errorMessage}</p>}

        <button
          type="submit"
          style={{
            padding: "10px",
            fontSize: "16px",
            backgroundColor: "#007BFF",
            color: "#fff",
            border: "none",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Register
        </button>
      </form>
    </div>
  );
};

export default Register;
