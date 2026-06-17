import type { PropsWithChildren } from "react";
import { NavLink } from "react-router-dom";

export function Layout({ children }: PropsWithChildren) {
  return (
    <div className="app-shell">
      <nav className="tabs" aria-label="Navigation">
        <NavLink
          to="/"
          className={({ isActive }) => (isActive ? "active" : "")}
        >
          Home
        </NavLink>
        <NavLink
          to="/profile"
          className={({ isActive }) => (isActive ? "active" : "")}
        >
          Profile
        </NavLink>
        <NavLink
          to="/notes"
          className={({ isActive }) => (isActive ? "active" : "")}
        >
          Notes
        </NavLink>
      </nav>
      {children}
    </div>
  );
}
