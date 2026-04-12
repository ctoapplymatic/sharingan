"use client";

import { useEffect, useState } from "react";

// BUG #2: This page does NOT check for authentication.
// It should redirect to /login if there's no token, but it doesn't.
// Any unauthenticated user can access the dashboard.

export default function DashboardPage() {
  const [user, setUser] = useState<{ email: string } | null>(null);

  useEffect(() => {
    // BUG: No auth check! Should verify token exists and is valid.
    // Should have:
    // const token = localStorage.getItem("token");
    // if (!token) { window.location.href = "/login"; return; }

    setUser({ email: "user@example.com" });
  }, []);

  return (
    <main>
      <h1>Dashboard</h1>
      {user ? (
        <div>
          <p>Welcome, {user.email}!</p>
          <h2>Your Stats</h2>
          <ul>
            <li>Projects: 5</li>
            <li>Tasks: 12</li>
            <li>Completed: 8</li>
          </ul>
          <button
            onClick={() => {
              localStorage.removeItem("token");
              window.location.href = "/login";
            }}
          >
            Log Out
          </button>
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </main>
  );
}
