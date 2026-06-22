import React from "react";

function Header({ theme, setTheme }) {
  const themes = [
    {
      name: "cyberpunk",
      color: "#00d4ff",
    },
    {
      name: "matrix",
      color: "#00ff66",
    },
    {
      name: "crimson",
      color: "#ff2a2a",
    },
    {
      name: "solaris",
      color: "#ffb700",
    },
  ];

  return (
    <header className="header">
      {/* Logo Section */}
      <div className="header-left">
        <h1 className="logo">
          CYBERMATE
        </h1>

        <p className="subtitle">
          AGENTIC SECURITY OPERATIONS CENTER
        </p>
      </div>

      {/* Navigation */}
      <nav className="header-nav">
        <a href="#dashboard">Dashboard</a>
        <a href="#pipeline">Pipeline</a>
        <a href="#feed">Live Feed</a>
        <a href="#alerts">Alerts</a>
      </nav>

      {/* Theme Switcher */}
      <div className="theme-buttons">
        {themes.map((item) => (
          <button
            key={item.name}
            className={`theme-btn ${
              theme === item.name ? "active-theme" : ""
            }`}
            style={{
              background: item.color,
            }}
            onClick={() =>
              setTheme(item.name)
            }
            title={item.name}
          />
        ))}
      </div>
    </header>
  );
}

export default Header;
