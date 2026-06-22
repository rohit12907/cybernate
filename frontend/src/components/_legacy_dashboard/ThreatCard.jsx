import React from "react";
import {
  FaBug,
  FaShieldAlt,
  FaExclamationTriangle,
  FaGlobe,
} from "react-icons/fa";

function ThreatCard({ threat }) {
  const getSeverityColor = (severity) => {
    switch (severity?.toLowerCase()) {
      case "critical":
        return "#ff3366";
      case "high":
        return "#ff9500";
      case "medium":
        return "#ffd700";
      case "low":
        return "#00ff88";
      default:
        return "#00d4ff";
    }
  };

  const getStatusColor = (status) => {
    switch (status?.toLowerCase()) {
      case "blocked":
        return "#00ff88";
      case "investigating":
        return "#ff9500";
      case "monitoring":
        return "#00d4ff";
      default:
        return "#82b3d1";
    }
  };

  return (
    <div
      className="threat-card"
      style={{
        borderLeft: `4px solid ${getSeverityColor(
          threat.severity
        )}`,
      }}
    >
      <div className="threat-header">
        <div className="threat-icon">
          <FaBug />
        </div>

        <div className="threat-main">
          <h3 className="threat-title">
            {threat.type}
          </h3>

          <p className="threat-ip">
            <FaGlobe /> {threat.ip}
          </p>
        </div>

        <div
          className="severity-badge"
          style={{
            color: getSeverityColor(
              threat.severity
            ),
            borderColor: getSeverityColor(
              threat.severity
            ),
          }}
        >
          <FaExclamationTriangle />
          {threat.severity}
        </div>
      </div>

      <div className="threat-footer">
        <div
          className="status-badge"
          style={{
            color: getStatusColor(
              threat.status
            ),
            borderColor: getStatusColor(
              threat.status
            ),
          }}
        >
          <FaShieldAlt />
          {threat.status}
        </div>
      </div>
    </div>
  );
}

export default ThreatCard;
