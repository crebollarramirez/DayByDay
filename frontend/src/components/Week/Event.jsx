import React, { useState, useEffect } from "react";
import "../../styles/eventStyle.css";
import api from '../../api';

export function Event({ event, getWeek }) {
  // Add local state to manage completed status
  const [isCompleted, setIsCompleted] = useState(event.completed);

  const setStatus = async (event) => {
    try {
      const response = await api.put(
        `api/all/status/${event.title}/${event.item_type}`,
        { completed: !isCompleted }
      );

      if (response.status === 204) {
        setIsCompleted(!isCompleted); // Update local state
        console.log("Todo was completed or undo successfully");
      } else {
        console.error("failed");
      }
    } catch (error) {
      console.error("Failed to set task status", error);
    }
    getWeek();
  };

  const onDelete = async (event) => {
    console.log(event)
    try {
      const response = await api.delete(
        `api/tasks/delete/${event.item_id}/${event.item_type}`
      );
    } catch (error) {
      console.log("Failed to delete the task");
    }
    getWeek();
  };

  const parseTimeFrame = (timeFrame) => {
    const startTime = timeFrame[0];
    const endTime = timeFrame[1];

    const startRow = convertToRow(startTime);
    const endRow = convertToRow(endTime);

    return { startRow, endRow };
  };

  // Helper function to convert military time string to grid row
  const convertToRow = (time) => {
    const [hour, minute] = time.split(":").map(Number);

    return hour + 1; // Convert 0-based index to 1-based grid row
  };

  const { startRow, endRow } = parseTimeFrame(event.timeFrame);

  return (
    <div
      className="event-container"
      style={{
        gridRow: `${startRow} / ${endRow}`, // Set the grid row based on the parsed times
      }}
    >
      <div className="event">
        <div className="heading">
          {/* Conditionally apply the line-through style */}
          <h3
            className="event-item"
            style={{ textDecoration: isCompleted ? "line-through" : "none" }}
          >
            {event.title}
          </h3>
          <p className="event-item">
            {event.timeFrame[0]} - {event.timeFrame[1]}
          </p>
        </div>
        <p
          className="event-item"
          style={{ textDecoration: isCompleted ? "line-through" : "none" }}
        >
          {event.content}
        </p>
        <div className="buttons">
          <button className="" onClick={() => onDelete(event)}>&#x2715;</button>
          <button>Edit</button>
          <button className="check" onClick={() => setStatus(event)}>&#10003;</button>
        </div>
      </div>
    </div>
  );
}
