import React, { useState, useEffect } from "react";
import "../../styles/eventStyle.css";

export function Event({ title, content, timeFrame }) {
    const parseTimeFrame = (timeFrame) => {
        const [startTime, endTime] = timeFrame.split(" - ");
        
        const startRow = convertToRow(startTime);
        const endRow = convertToRow(endTime);
        
        return { startRow, endRow };
      };
      
      // Helper function to convert time string to grid row
      const convertToRow = (time) => {
        const [timeString, period] = time.split(" ");
        let [hour, minute] = timeString.split(":").map(Number);
        
        if (period === "PM" && hour !== 12) {
          hour += 12; // Convert PM hour to 24-hour format
        } else if (period === "AM" && hour === 12) {
          hour = 0; // Convert 12 AM to 0 hours
        }
        
        return hour + 1; // Convert 0-based index to 1-based grid row
      };

      
  const { startRow, endRow } = parseTimeFrame(timeFrame);

  return (
    <div
      className="event-container"
      style={{
        gridRow: `${startRow} / ${endRow}`, // Set the grid row based on the parsed times
      }}
    >
      <h3 className="event-item">{title}</h3>
      <p className="event-item">{content}</p>
      <p className="event-item">{timeFrame}</p>
    </div>
  );
}
