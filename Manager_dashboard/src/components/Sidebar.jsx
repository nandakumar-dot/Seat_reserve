import { useState } from "react";
import "./Sidebar.css";

const Sidebar = () => {
  const [managerName, setManagerName] = useState("");
  const [selectedDate, setSelectedDate] = useState("");
  const [employees, setEmployees] = useState([
    { id: 1, manager: "Alice", name: "John Doe", seat: "A12", time: "10:00 AM", date: "2025-02-01" },
    { id: 2, manager: "Alice", name: "Jane Smith", seat: "B5", time: "02:00 PM", date: "2025-02-01" },
    { id: 3, manager: "Bob", name: "David Johnson", seat: "C8", time: "04:00 PM", date: "2025-02-02" },
  ]);

  // Filter employees based on selected manager and date
  const filteredEmployees = employees.filter(
    (emp) => emp.manager.toLowerCase() === managerName.toLowerCase() && emp.date === selectedDate
  );

  return (
    <div className="sidebar">
      {/* Section 1: Manager Name & Date Picker */}
      <div className="sidebar-section">
      <div class="profile-div">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
      <path strokeLinecap="round" strokeLinejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
      </svg>
        <h3>Manager Name</h3>
      </div>
        <div className="wallet">
        <p className="wallet-field">Wallet : </p>
        <p className="wallet-value"> 100</p>
        </div>
        <p>Pick a date : </p>
        <input
          type="date"
          value={selectedDate}
          onChange={(e) => setSelectedDate(e.target.value)}
          className="date-picker"
        />
      </div>

      {/* Section 2: Employee Table */}
      <div className="sidebar-section">
        <h3>Employees Under Manager</h3>
        <table className="employee-table">
          <thead>
            <tr>
              <th>Name</th>
              <th>Seat</th>
              <th>Time Slot</th>
            </tr>
          </thead>
          <tbody>
            {filteredEmployees.length > 0 ? (
              filteredEmployees.map((employee) => (
                <tr key={employee.id}>
                  <td>{employee.name}</td>
                  <td>{employee.seat}</td>
                  <td>{employee.time}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="3" className="no-data">No employees found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Sidebar;
