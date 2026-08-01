import { useEffect, useState } from "react";

function AgentDashboard({ onLogout }) {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [refreshing, setRefreshing] = useState(false);

  useEffect(() => {
  const fetchTickets = async () => {
    const token = localStorage.getItem("token");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/agent/tickets",
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      const data = await response.json();

      if (!response.ok) {
        console.error(data);
        return;
      }

      setTickets(data.tickets);
      setLoading(false);
    } catch (error) {
  console.error("Failed to load tickets:", error);
  setError("Failed to load assigned tickets.");
  setLoading(false);
}
  };

  fetchTickets();
}, []);


const refreshTickets = async () => {
  setRefreshing(true);
  setError("");

  const token = localStorage.getItem("token");

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/agent/tickets",
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );

    const data = await response.json();

    if (!response.ok) {
      setError(data.detail || "Failed to refresh tickets.");
      return;
    }

    setTickets(data.tickets);
  } catch (error) {
    console.error("Failed to refresh tickets:", error);
    setError("Failed to refresh assigned tickets.");
  } finally {
    setRefreshing(false);
  }
};


const updateTicketStatus = async (ticketId, newStatus) => {
    const confirmed = window.confirm(
  `Change ticket status to "${newStatus}"?`
);

if (!confirmed) return;

  const token = localStorage.getItem("token");

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/tickets/${ticketId}/status`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          status: newStatus,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      alert(data.detail || "Failed to update ticket status");
      return;
    }

    setTickets((currentTickets) =>
      currentTickets.map((ticket) =>
        ticket.id === ticketId
          ? { ...ticket, status: newStatus }
          : ticket
      )
    );

    alert("Ticket status updated successfully");
  } catch (error) {
    console.error("Failed to update ticket status:", error);
    alert("Could not update ticket status");
  }
};

  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div>
          <h1>AI Helpdesk</h1>
          <p>Agent Dashboard</p>
        </div>

        <button className="logout-btn" onClick={onLogout}>
          Logout
        </button>
      </header>

      <div className="users-section">
  <div className="section-header">
    <h2>Assigned Tickets</h2>

    <button
      className="refresh-btn"
      onClick={refreshTickets}
      disabled={refreshing}
    >
      {refreshing ? "Refreshing..." : "Refresh"}
    </button>
  </div>

  {loading ? (
  <p>Loading tickets...</p>
) : error ? (
  <p className="error-message">{error}</p>
) : tickets.length === 0 ? (
  <div className="empty-state">
  <h3>No assigned tickets</h3>
  <p>There are currently no support tickets assigned to you.</p>
</div>
) : (
    <div className="table-container">
      <table className="users-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Title</th>
            <th>Category</th>
            <th>Priority</th>
            <th>Score</th>
            <th>Status</th>
          </tr>
        </thead>

        <tbody>
          {tickets.map((ticket) => (
            <tr key={ticket.id}>
              <td>{ticket.id}</td>
              <td>{ticket.title}</td>
              <td>{ticket.category || "Pending"}</td>
              <td>
              <span
                 className={`priority priority-${ticket.priority.toLowerCase()}`}
                >
                 {ticket.priority}
                </span>
                </td>
              <td>{ticket.priority_score ?? "-"}</td>
              <td>
  <select
    value={ticket.status}
    onChange={(e) =>
  updateTicketStatus(ticket.id, e.target.value)
}
  >
    <option value="Open">Open</option>
    <option value="In Progress">In Progress</option>
    <option value="Resolved">Resolved</option>
    <option value="Closed">Closed</option>
  </select>
</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )}
</div>
    </div>
  );
}

export default AgentDashboard;