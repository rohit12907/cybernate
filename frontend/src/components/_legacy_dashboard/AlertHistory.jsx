import React from "react";
import {
  FaShieldAlt,
  FaExclamationTriangle,
  FaCheckCircle,
} from "react-icons/fa";

function AlertHistory({ alerts = [] }) {
  const getSeverityClass = (severity) => {
    switch (severity?.toLowerCase()) {
      case "critical":
        return "badge-critical";
      case "high":
        return "badge-high";
      case "medium":
        return "badge-medium";
      case "low":
        return "badge-low";
      default:
        return "badge-low";
    }
  };

  return (
    <section className="alert-history-section" id="alerts">
      <div className="alert-header">
        <h2>
          <FaShieldAlt /> ALERT HISTORY
        </h2>
      </div>

      <div className="table-wrapper">
        <table className="alert-table">
          <thead>
            <tr>
              <th>TIME</th>
              <th>THREAT</th>
              <th>SEVERITY</th>
              <th>ACTION</th>
              <th>STATUS</th>
            </tr>
          </thead>

          <tbody>
            {alerts.length > 0 ? (
              alerts.map((alert) => (
                <tr key={alert.id}>
                  <td>{alert.timestamp}</td>

                  <td>{alert.threat}</td>

                  <td>
                    <span
                      className={`badge ${getSeverityClass(
                        alert.severity
                      )}`}
                    >
                      <FaExclamationTriangle />
                      {alert.severity}
                    </span>
                  </td>

                  <td>{alert.action}</td>

                  <td>
                    <span className="status-success">
                      <FaCheckCircle />
                      Completed
                    </span>
                  </td>
                </tr>
              ))
            ) : (
              <tr>
                <td
                  colSpan="5"
                  className="empty-alerts"
                >
                  No alerts available
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </section>
  );
}

export default AlertHistory;
