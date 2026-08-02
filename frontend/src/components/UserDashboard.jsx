import { useEffect, useState } from "react";

function UserDashboard({ onLogout }) {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [refreshing, setRefreshing] = useState(false);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
  const fetchMyTickets = async () => {
    const token = localStorage.getItem("token");

    try {
      const response = await fetch(
  `${import.meta.env.VITE_API_URL}/tickets/my`,
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
setError("Failed to load your tickets.");
setLoading(false);
    }
  };

  fetchMyTickets();
}, []);


const refreshTickets = async () => {
  setRefreshing(true);
  setError("");

  const token = localStorage.getItem("token");

  try {
    const response = await fetch(
  `${import.meta.env.VITE_API_URL}/tickets/my`,
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
    setError("Failed to refresh your tickets.");
  } finally {
    setRefreshing(false);
  }
};


const createTicket = async (e) => {
  e.preventDefault();
  setSubmitting(true);

  console.log("Create Ticket API:", import.meta.env.VITE_API_URL);

  const token = localStorage.getItem("token");

  try {
    const response = await fetch(
  `${import.meta.env.VITE_API_URL}/tickets`,
  {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          title,
          description,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      alert(data.detail || "Failed to create ticket");
      return;
    }

    alert("Ticket created successfully");

    setTitle("");
    setDescription("");

    if (data.ticket) {
      setTickets((currentTickets) => [
        data.ticket,
        ...currentTickets,
      ]);
    }
  } catch (error) {
    console.error("Failed to create ticket:", error);
    alert("Could not create ticket");
  }finally {
  setSubmitting(false);
}
};




  return (
    <div className="dashboard">
      <header className="dashboard-header">
        <div>
  <h1>AI Helpdesk</h1>
  <p>Submit and track your support requests</p>
</div>

        <button className="logout-btn" onClick={onLogout}>
          Logout
        </button>
      </header>

      <div className="users-section">
  <div className="section-header">
    <h2>My Tickets</h2>

    <button
      className="refresh-btn"
      onClick={refreshTickets}
      disabled={refreshing}
    >
      {refreshing ? "Refreshing..." : "Refresh"}
    </button>
  </div>

  <form onSubmit={createTicket}>
    <div className="form-group">
      <label>Title</label>
      <input
        type="text"
        placeholder="Enter ticket title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        required
      />
    </div>

    <div className="form-group">
      <label>Description</label>
      <textarea
        placeholder="Describe your problem"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        required
        rows="5"
      />
    </div>

    <button
  type="submit"
  className="login-button"
  disabled={submitting}
>
  {submitting ? "Creating..." : "Create Ticket"}
</button>
  </form>
</div>



      <div className="users-section">
        <h2>My Tickets</h2>

        {loading ? (
  <p>Loading tickets...</p>
) : error ? (
  <p className="error-message">{error}</p>
) : tickets.length === 0 ? (
  <div className="empty-state">
  <h3>No tickets yet</h3>
  <p>Create your first support ticket using the form above.</p>
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
  <span
    className={`status status-${ticket.status
      .toLowerCase()
      .replace(/\s+/g, "-")}`}
  >
    {ticket.status}
  </span>
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

export default UserDashboard;