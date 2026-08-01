import { useEffect, useState } from "react";
import {
  ResponsiveContainer,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";

function AdminDashboard({ onLogout }) {
  console.log("AdminDashboard component rendered");
  const [stats, setStats] = useState(null);
  const [users, setUsers] = useState([]);
  const [tickets, setTickets] = useState([]);
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [refreshing, setRefreshing] = useState(false);
  const [ticketSearch, setTicketSearch] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [priorityFilter, setPriorityFilter] = useState("all");
  const [sortOrder, setSortOrder] = useState("default");


  useEffect(() => {
      console.log("AdminDashboard useEffect running");
    const fetchStats = async () => {
      const token = localStorage.getItem("token");

      try {
        const response = await fetch(
          "http://127.0.0.1:8000/admin/stats",
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

        setStats(data);
      } catch (error) {
  console.error("Failed to load stats:", error);
  setError("Failed to load dashboard data.");
}
    };

    const fetchUsers = async () => {
    const token = localStorage.getItem("token");

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/admin/users",
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

    setUsers(data.users);
  } catch (error) {
    console.error("Failed to load users:", error);
  }
};

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
  } catch (error) {
    console.error("Failed to load tickets:", error);
  }
};

const fetchAgents = async () => {
  const token = localStorage.getItem("token");

  try {
    const response = await fetch(
      "http://127.0.0.1:8000/admin/agents",
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

    setAgents(data.agents);
  } catch (error) {
    console.error("Failed to load agents:", error);
  }
};

const loadDashboard = async () => {
  await Promise.all([
    fetchStats(),
    fetchUsers(),
    fetchTickets(),
    fetchAgents(),
  ]);

  setLoading(false);
};

loadDashboard();
  }, []);


  const refreshDashboard = async () => {
  setRefreshing(true);
  setError("");

  const token = localStorage.getItem("token");

  try {
    const [statsResponse, usersResponse, ticketsResponse, agentsResponse] =
      await Promise.all([
        fetch("http://127.0.0.1:8000/admin/stats", {
          headers: { Authorization: `Bearer ${token}` },
        }),
        fetch("http://127.0.0.1:8000/admin/users", {
          headers: { Authorization: `Bearer ${token}` },
        }),
        fetch("http://127.0.0.1:8000/agent/tickets", {
          headers: { Authorization: `Bearer ${token}` },
        }),
        fetch("http://127.0.0.1:8000/admin/agents", {
          headers: { Authorization: `Bearer ${token}` },
        }),
      ]);

    if (
      !statsResponse.ok ||
      !usersResponse.ok ||
      !ticketsResponse.ok ||
      !agentsResponse.ok
    ) {
      setError("Failed to refresh dashboard data.");
      return;
    }

    const statsData = await statsResponse.json();
    const usersData = await usersResponse.json();
    const ticketsData = await ticketsResponse.json();
    const agentsData = await agentsResponse.json();

    setStats(statsData);
    setUsers(usersData.users);
    setTickets(ticketsData.tickets);
    setAgents(agentsData.agents);
  } catch (error) {
    console.error("Failed to refresh dashboard:", error);
    setError("Failed to refresh dashboard data.");
  } finally {
    setRefreshing(false);
  }
};


  const updateUserRole = async (userId, newRole) => {
    const confirmed = window.confirm(
  `Are you sure you want to change this user's role to "${newRole}"?`
);

if (!confirmed) return;

  const token = localStorage.getItem("token");

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/admin/users/${userId}/role`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          role: newRole,
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      alert(data.detail || "Failed to update role");
      return;
    }

    setUsers((currentUsers) =>
      currentUsers.map((user) =>
        user.id === userId
          ? { ...user, role: newRole }
          : user
      )
    );

    alert("User role updated successfully");
  } catch (error) {
    console.error("Failed to update role:", error);
    alert("Could not update user role");
  }
};

const assignTicket = async (ticketId, agentId) => {
  if (!agentId) return;
  const confirmed = window.confirm(
  "Are you sure you want to assign this ticket to the selected agent?"
);

if (!confirmed) return;

  const token = localStorage.getItem("token");

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/tickets/${ticketId}/assign`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          agent_id: Number(agentId),
        }),
      }
    );

    const data = await response.json();

    if (!response.ok) {
      alert(data.detail || "Failed to assign ticket");
      return;
    }

    setTickets((currentTickets) =>
      currentTickets.map((ticket) =>
        ticket.id === ticketId
          ? { ...ticket, assigned_agent: Number(agentId) }
          : ticket
      )
    );

    alert("Ticket assigned successfully");
  } catch (error) {
    console.error("Failed to assign ticket:", error);
    alert("Could not assign ticket");
  }
};

const filteredTickets = tickets.filter((ticket) => {
  const search = ticketSearch.toLowerCase();

  const matchesSearch =
    ticket.title?.toLowerCase().includes(search) ||
    ticket.category?.toLowerCase().includes(search) ||
    ticket.priority?.toLowerCase().includes(search) ||
    ticket.status?.toLowerCase().includes(search);

  const matchesStatus =
    statusFilter === "all" ||
    ticket.status === statusFilter;

  const matchesPriority =
    priorityFilter === "all" ||
    ticket.priority === priorityFilter;

  return matchesSearch && matchesStatus && matchesPriority;
});

const priorityRank = {
  Critical: 4,
  High: 3,
  Medium: 2,
  Low: 1,
};

if (sortOrder === "priority-high") {
  filteredTickets.sort(
    (a, b) => priorityRank[b.priority] - priorityRank[a.priority]
  );
}

if (sortOrder === "priority-low") {
  filteredTickets.sort(
    (a, b) => priorityRank[a.priority] - priorityRank[b.priority]
  );
}

const ticketStatusData = [
  {
    name: "Open",
    value: stats?.open_tickets || 0,
  },
  {
    name: "In Progress",
    value: stats?.in_progress_tickets || 0,
  },
  {
    name: "Resolved",
    value: stats?.resolved_tickets || 0,
  },
  {
    name: "Closed",
    value: stats?.closed_tickets || 0,
  },
];

const ticketPriorityData = [
  {
    name: "Critical",
    value: tickets.filter((t) => t.priority === "Critical").length,
  },
  {
    name: "High",
    value: tickets.filter((t) => t.priority === "High").length,
  },
  {
    name: "Medium",
    value: tickets.filter((t) => t.priority === "Medium").length,
  },
  {
    name: "Low",
    value: tickets.filter((t) => t.priority === "Low").length,
  },
];

const PIE_COLORS = [
  "#dc2626", // Critical
  "#ea580c", // High
  "#eab308", // Medium
  "#16a34a", // Low
];

const agentPerformanceData = agents.map((agent) => ({
  name: agent.name,
  tickets: tickets.filter(
    (ticket) => ticket.assigned_agent === agent.id
  ).length,
}));

 return (
  <div className="dashboard">
    <header className="dashboard-header">
      <div>
      <h1>AI Helpdesk</h1>
      <p>Monitor users, agents, and support ticket operations</p>
      </div>

      <div>
        <button
          className="refresh-btn"
          onClick={refreshDashboard}
          disabled={refreshing}
          style={{ marginRight: "10px" }}
        >
          {refreshing ? "Refreshing..." : "Refresh"}
        </button>

        <button className="logout-btn" onClick={onLogout}>
          Logout
        </button>
      </div>
    </header>

    {loading ? (
      <p>Loading dashboard...</p>
    ) : error ? (
      <p className="error-message">{error}</p>
    ) : (
      <>
        {/* Statistics */}
        <div className="stats-grid">
          <div className="stat-card">
            <h3>Total Users</h3>
            <p>{stats.total_users}</p>
          </div>

          <div className="stat-card">
            <h3>Total Agents</h3>
            <p>{stats.total_agents}</p>
          </div>

          <div className="stat-card">
            <h3>Total Tickets</h3>
            <p>{stats.total_tickets}</p>
          </div>

          <div className="stat-card">
            <h3>Open</h3>
            <p>{stats.open_tickets}</p>
          </div>

          <div className="stat-card">
            <h3>In Progress</h3>
            <p>{stats.in_progress_tickets}</p>
          </div>

          <div className="stat-card">
            <h3>Resolved</h3>
            <p>{stats.resolved_tickets}</p>
          </div>

          <div className="stat-card">
            <h3>Closed</h3>
            <p>{stats.closed_tickets}</p>
          </div>

          <div className="stat-card">
            <h3>Critical</h3>
            <p>{stats.critical_tickets}</p>
          </div>
        </div>

        <div className="users-section">
  <h2>Dashboard Analytics</h2>

  <div className="charts-grid">
    <div className="chart-card">
      <h3>Ticket Status Overview</h3>

      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={ticketStatusData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="name" />
          <YAxis />
          <Tooltip />
          <Bar dataKey="value" radius={[8, 8, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>

    <div className="chart-card">
      <h3>Priority Distribution</h3>

      <ResponsiveContainer width="100%" height={300}>
        <PieChart>
          <Pie
            data={ticketPriorityData}
            dataKey="value"
            nameKey="name"
            outerRadius={90}
            label
          >
            {ticketPriorityData.map((entry, index) => (
              <Cell
                key={index}
                fill={PIE_COLORS[index % PIE_COLORS.length]}
              />
            ))}
          </Pie>

          <Tooltip />
          <Legend />
        </PieChart>
      </ResponsiveContainer>
    </div>
  </div>
</div>

<div className="chart-card">
  <h3>Agent Performance</h3>

  <ResponsiveContainer width="100%" height={300}>
    <BarChart data={agentPerformanceData}>
      <CartesianGrid strokeDasharray="3 3" />
      <XAxis dataKey="name" />
      <YAxis />
      <Tooltip />
      <Bar dataKey="tickets" radius={[8, 8, 0, 0]} />
    </BarChart>
  </ResponsiveContainer>
</div>

        {/* User Management */}
        <div className="users-section">
          <h2>User Management</h2>

          <div className="table-container">
            <table className="users-table">
              <thead>
                <tr>
                  <th>ID</th>
                  <th>Name</th>
                  <th>Email</th>
                  <th>Role</th>
                  <th>Action</th>
                </tr>
              </thead>

              <tbody>
                {users.map((user) => (
                  <tr key={user.id}>
                    <td>{user.id}</td>
                    <td>{user.name}</td>
                    <td>{user.email}</td>
                    <td>{user.role}</td>

                    <td>
                      <select
                        value={user.role}
                        disabled={user.email === "test@example.com"}
                        onChange={(e) =>
                          updateUserRole(user.id, e.target.value)
                        }
                      >
                        <option value="user">User</option>
                        <option value="agent">Agent</option>
                        <option value="admin">Admin</option>
                      </select>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>

        {/* Ticket Management */}
        <div className="users-section">
  <div className="section-header">
    <div>
  <h2>Ticket Management</h2>
  <p className="ticket-count">
    Showing {filteredTickets.length} of {tickets.length} tickets
  </p>
</div>

    <input
      type="text"
      className="ticket-search"
      placeholder="Search tickets..."
      value={ticketSearch}
      onChange={(e) => setTicketSearch(e.target.value)}
    />

<select
  className="status-filter"
  value={statusFilter}
  onChange={(e) => setStatusFilter(e.target.value)}
>
  <option value="all">All Status</option>
  <option value="Open">Open</option>
  <option value="In Progress">In Progress</option>
  <option value="Resolved">Resolved</option>
  <option value="Closed">Closed</option>
</select>
<select
  className="status-filter"
  value={priorityFilter}
  onChange={(e) => setPriorityFilter(e.target.value)}
>
  <option value="all">All Priority</option>
  <option value="Critical">Critical</option>
  <option value="High">High</option>
  <option value="Medium">Medium</option>
  <option value="Low">Low</option>
</select>
<select
  className="status-filter"
  value={sortOrder}
  onChange={(e) => setSortOrder(e.target.value)}
>
  <option value="default">Sort By</option>
  <option value="priority-high">Priority: High to Low</option>
  <option value="priority-low">Priority: Low to High</option>
</select>

{(ticketSearch ||
  statusFilter !== "all" ||
  priorityFilter !== "all" ||
  sortOrder !== "default") && (
  <button
  className="clear-search-btn"
  onClick={() => {
    setTicketSearch("");
    setStatusFilter("all");
    setPriorityFilter("all");
    setSortOrder("default");
  }}
>
  Clear
</button>
)}
  </div>

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
                  <th>Assigned Agent</th>
                </tr>
              </thead>

              <tbody>
                {filteredTickets.length === 0 && (
  <tr>
    <td colSpan="7" className="no-results">
      No tickets match your search or filters.
    </td>
  </tr>
)}
                {filteredTickets.map((ticket) => (
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

                    <td>
                      <select
                        value={ticket.assigned_agent ?? ""}
                        onChange={(e) =>
                          assignTicket(ticket.id, e.target.value)
                        }
                      >
                        <option value="">Unassigned</option>

                        {agents.map((agent) => (
                          <option key={agent.id} value={agent.id}>
                            {agent.name}
                          </option>
                        ))}
                      </select>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </>
    )}
  </div>
);
}

export default AdminDashboard;