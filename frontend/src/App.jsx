import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Register from "./pages/Register";

function App() {
  return (
    <div>
      {/* Welcome message */}
      <div style={{ textAlign: 'center', marginTop: '20px' }}>
        <h1>Welcome to the Coffee Seat Reservation App</h1>
      </div>

      {/* Routing logic */}
      <BrowserRouter>
        <Routes>
          {/* Route for Login */}
          <Route path="/" element={<Login />} />
          {/* Route for Register */}
          <Route path="/register" element={<Register />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
}

export default App;

