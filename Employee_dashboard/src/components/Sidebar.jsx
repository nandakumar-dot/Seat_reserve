import { useState } from "react";
import "./Sidebar.css";

const Sidebar = () => {
  const [userName, setUserName] = useState("");
  const [selectedDate, setSelectedDate] = useState("");
  const [bookings, setBookings] = useState([
    { id: 1, name: "Alice", seat: "A12", time: "10:00 AM", date: "2025-02-01" },
    { id: 2, name: "Alice", seat: "B5", time: "02:00 PM", date: "2025-02-03" },
    { id: 3, name: "Bob", seat: "C8", time: "04:00 PM", date: "2025-02-01" },
  ]);

  // Filter bookings based on selected date and user name
  const filteredBookings = bookings.filter(
    (booking) => booking.name.toLowerCase() === userName.toLowerCase() && booking.date === selectedDate
  );

  return (
    <div className="sidebar">
      {/* Section 1: Date Picker */}
      <div className="sidebar-section">
      <div class="profile-div">
      <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
      <path strokeLinecap="round" strokeLinejoin="round" d="M17.982 18.725A7.488 7.488 0 0 0 12 15.75a7.488 7.488 0 0 0-5.982 2.975m11.963 0a9 9 0 1 0-11.963 0m11.963 0A8.966 8.966 0 0 1 12 21a8.966 8.966 0 0 1-5.982-2.275M15 9.75a3 3 0 1 1-6 0 3 3 0 0 1 6 0Z" />
      </svg>
      <h3>User Details</h3>
      </div>
      <p>Pick a date : </p>
        <input
          type="date"
          value={selectedDate}
          onChange={(e) => setSelectedDate(e.target.value)}
          className="date-picker"
        />
      </div>

      {/* Section 2: Booking History */}
      <div className="sidebar-section">
        <h3>Previous Bookings</h3>
        <table className="booking-table">
          <thead>
            <tr>
              <th>Seat</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            {filteredBookings.length > 0 ? (
              filteredBookings.map((booking) => (
                <tr key={booking.id}>
                  <td>{booking.seat}</td>
                  <td>{booking.time}</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="2" className="no-data">No bookings found</td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default Sidebar;