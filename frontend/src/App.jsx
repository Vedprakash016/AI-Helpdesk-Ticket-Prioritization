import { useState } from "react";
import "./App.css";
import AdminDashboard from "./components/AdminDashboard";
import AgentDashboard from "./components/AgentDashboard";
import UserDashboard from "./components/UserDashboard";

function App() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [role, setRole] = useState(localStorage.getItem("role") || "");

  const handleSubmit = async (e) => {
  e.preventDefault();

  try {
    const response = await fetch("http://127.0.0.1:8000/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
        password,
      }),
    });

    const data = await response.json();

    if (!response.ok) {
      alert(data.detail || "Login failed");
      return;
    }

    console.log("Login successful:", data);

    localStorage.setItem("token", data.access_token);
    localStorage.setItem("role", data.user.role);

    setRole(data.user.role);
    
  } catch (error) {
    console.error(error);
    alert("Cannot connect to backend");
  }
};

if (role === "admin") {
  const handleLogout = () => {
    const confirmed = window.confirm(
      "Are you sure you want to logout?"
    );

    if (!confirmed) return;

    localStorage.removeItem("token");
    localStorage.removeItem("role");
    setRole("");
  };

  return <AdminDashboard onLogout={handleLogout} />;
}


if (role === "agent") {
  const handleLogout = () => {
  const confirmed = window.confirm(
    "Are you sure you want to logout?"
  );

  if (!confirmed) return;

  localStorage.removeItem("token");
  localStorage.removeItem("role");
  setRole("");
};

  return <AgentDashboard onLogout={handleLogout} />;
}


if (role === "user") {
  const handleLogout = () => {
  const confirmed = window.confirm(
    "Are you sure you want to logout?"
  );

  if (!confirmed) return;

  localStorage.removeItem("token");
  localStorage.removeItem("role");
  setRole("");
};

  return <UserDashboard onLogout={handleLogout} />;
}


  return (
    <div className="login-page">
      <div className="login-card">
        <div className="logo">AI</div>

        <h1>AI Helpdesk</h1>

        <p className="subtitle">
          Intelligent Ticket Prioritization System
        </p>

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Email</label>

            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label>Password</label>

            <input
              type="password"
              placeholder="Enter your password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="login-button">
            Sign In
          </button>
        </form>

        <p className="footer-text">
          AI-powered support ticket management
        </p>
      </div>
    </div>
  );
}

export default App;