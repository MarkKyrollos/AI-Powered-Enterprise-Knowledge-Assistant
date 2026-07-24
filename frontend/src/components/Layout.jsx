import React from "react";
import { NavLink, useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

const navItems = [
  { to: "/", label: "Chat", icon: "💬" },
  { to: "/documents", label: "Documents", icon: "📄" },
  { to: "/profile", label: "Profile", icon: "👤" },
];

export default function Layout({ children }) {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <div className="flex h-screen w-full overflow-hidden">
      <aside className="flex w-64 shrink-0 flex-col border-r border-ink/10 bg-white">
        <div className="px-6 py-6">
          <div className="flex items-center gap-2">
            <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-ink text-paper font-mono text-sm font-semibold">
              EK
            </div>
            <span className="font-semibold tracking-tight">Knowledge Assistant</span>
          </div>
        </div>
        <nav className="flex-1 space-y-1 px-3">
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              className={({ isActive }) =>
                `flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition ${
                  isActive
                    ? "bg-ink text-paper"
                    : "text-ink/70 hover:bg-ink/5 hover:text-ink"
                }`
              }
            >
              <span>{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </nav>
        <div className="border-t border-ink/10 px-4 py-4">
          <p className="truncate text-xs text-ink/50">{user?.email}</p>
          <button
            onClick={handleLogout}
            className="mt-2 w-full rounded-lg border border-ink/15 px-3 py-2 text-left text-sm font-medium text-ink/70 hover:border-ink/30 hover:text-ink"
          >
            Sign out
          </button>
        </div>
      </aside>
      <main className="flex-1 overflow-y-auto">{children}</main>
    </div>
  );
}
