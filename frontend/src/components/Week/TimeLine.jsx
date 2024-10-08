import React from "react";
import "../../styles/timeLineStyle.css";

export function TimeLine() {
  const TimeMarkers = () => {
    const hours = [];

    for (let i = 0; i < 24; i++) {
      // Format the hour in 12-hour format with AM/PM
      const formattedHour = i % 12 === 0 ? 12 : i % 12;
      const amPm = i < 12 ? "AM" : "PM";

      hours.push(
        <div
          key={i}
          className="timeMarker"
          style={{
            gridRow: `${i + 1}`, // Set the grid row based on the hour index (1-based)
          }}
        >
          {formattedHour} {amPm}
        </div>
      );
    }

    return <>{hours}</>; // Return the array of markers
  };

  return (
    <div className="timeLine-container">
      <TimeMarkers />
    </div>
  );
}
