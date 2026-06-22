import React from "react";
import {
  FaShieldAlt,
  FaBug,
  FaRobot,
  FaExclamationTriangle,
} from "react-icons/fa";

function StatsBar({ stats }) {
  const cards = [
    {
      title: "Threats Detected",
      value: stats.threatsDetected,
      icon: <FaBug />,
      color: "#ff3366",
    },
    {
      title: "Threats Blocked",
      value: stats.threatsBlocked,
      icon: <FaShieldAlt />,
      color: "#00ff88",
    },
    {
      title: "Active Agents",
      value: stats.activeAgents,
      icon: <FaRobot />,
      color: "#00d4ff",
    },
    {
      title: "Risk Level",
      value: stats.riskLevel,
      icon: <FaExclamationTriangle />,
      color: "#ffd700",
    },
  ];

  return (
    <section className="stats-bar" id="dashboard">
      {cards.map((card, index) => (
        <div
          className="stat-card"
          key={index}
          style={{
            borderTop: `3px solid ${card.color}`,
          }}
        >
          <div
            className="stat-icon"
            style={{
              color: card.color,
            }}
          >
            {card.icon}
          </div>

          <div className="stat-content">
            <p className="stat-title">
              {card.title}
            </p>

            <h2
              className="stat-value"
              style={{
                color: card.color,
              }}
            >
              {card.value}
            </h2>
          </div>
        </div>
      ))}
    </section>
  );
}

export default StatsBar;
