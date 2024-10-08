import React, { useState, useEffect } from "react";
import "../../styles/eventStyle.css";

const parseTimeFrame = (timeFrame) => {
  const [start, end] = timeFrame.split(" - ");
  const startHour = parseInt(start.split(":")[0]);
  const startMinute =
    start.includes("PM") && startHour !== 12 ? startHour + 12 : startHour;
  const endHour = parseInt(end.split(":")[0]);
  const endMinute =
    end.includes("PM") && endHour !== 12 ? endHour + 12 : endHour;

  return {
    startRow: startMinute === 0 ? startHour : startHour + 1, // Shift down if minutes are present
    endRow: endMinute === 0 ? endHour : endHour + 1,
  };
};

export function Event({ title, content, timeFrame }) {
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
