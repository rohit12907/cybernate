import React from "react";
import {
  FaShieldAlt,
  FaEye,
  FaDatabase,
  FaChartLine,
  FaRobot,
  FaBell,
} from "react-icons/fa";

function PipelineView() {
  const stages = [
    {
      id: 1,
      title: "ATTACK DETECTION",
      subtitle: "Engine",
      icon: <FaShieldAlt />,
      color: "#ff3366",
    },
    {
      id: 2,
      title: "WATCHER",
      subtitle: "Agent",
      icon: <FaEye />,
      color: "#ff9500",
    },
    {
      id: 3,
      title: "THREAT INTEL",
      subtitle: "Analysis",
      icon: <FaDatabase />,
      color: "#a855f7",
    },
    {
      id: 4,
      title: "RISK ANALYZER",
      subtitle: "Scoring",
      icon: <FaChartLine />,
      color: "#ffd700",
    },
    {
      id: 5,
      title: "RESPONSE AGENT",
      subtitle: "Mitigation",
      icon: <FaRobot />,
      color: "#00ff88",
    },
    {
      id: 6,
      title: "NOTIFICATION",
      subtitle: "Center",
      icon: <FaBell />,
      color: "#00d4ff",
    },
  ];

  return (
    <section className="pipeline-wrapper" id="pipeline">
      <div className="pipeline-container">
        {stages.map((stage, index) => (
          <React.Fragment key={stage.id}>
            <div
              className="pipeline-stage"
              style={{
                borderColor: stage.color,
              }}
            >
              <div
                className="pipeline-icon"
                style={{
                  color: stage.color,
                }}
              >
                {stage.icon}
              </div>

              <h3>{stage.title}</h3>

              <p>{stage.subtitle}</p>

              <span className="stage-number">
                0{stage.id}
              </span>
            </div>

            {index !== stages.length - 1 && (
              <div className="pipeline-arrow">
                →
              </div>
            )}
          </React.Fragment>
        ))}
      </div>
    </section>
  );
}

export default PipelineView;
