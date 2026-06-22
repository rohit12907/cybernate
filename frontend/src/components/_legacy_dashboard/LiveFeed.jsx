import React from "react";
import ThreatCard from "./ThreatCard";
import { FaSatelliteDish } from "react-icons/fa";

function LiveFeed({ threats = [] }) {
  return (
    <section className="live-feed-section" id="feed">
      <div className="feed-header">
        <div className="feed-title">
          <FaSatelliteDish className="feed-icon" />
          <span>LIVE THREAT FEED</span>
        </div>

        <div className="live-indicator">
          <span className="live-dot"></span>
          LIVE
        </div>
      </div>

      <div className="live-feed">
        {threats.length > 0 ? (
          threats.map((threat) => (
            <ThreatCard
              key={threat.id}
              threat={threat}
            />
          ))
        ) : (
          <div className="empty-feed">
            <h3>No Active Threats</h3>
            <p>CyberMate is continuously monitoring network activity.</p>
          </div>
        )}
      </div>
    </section>
  );
}

export default LiveFeed;
