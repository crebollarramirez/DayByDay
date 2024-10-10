import React, { useState, useEffect } from "react";
import "../../styles/eventStyle.css";

export function Event({ title, content, timeFrame, isCompleted }) {
  const setStatus = async (task) => {
    try {
      const response = await api.put(
        `api/all/status/${task.title}/${task.item_type}`,
        { completed: !task.completed }
      );

      if (response.status === 204) {
        console.log("Todo was completed or undo successfully");
      } else {
        console.error("failed");
      }
    } catch (error) {
      console.error("Failed to set task status", error);
    }
    getWeek();
  };

  const onDelete = async (title, item_type) => {
    try {
      const response = await api.delete(
        `api/tasks/delete/${title}/${item_type}`
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

  const { startRow, endRow } = parseTimeFrame(timeFrame);

  return (
    <div
      className="event-container"
      style={{
        gridRow: `${startRow} / ${endRow}`, // Set the grid row based on the parsed times
      }}
    >
      <div className="event">
        <div className="heading">
          <h3 className="event-item">{title} </h3>
          <p className="event-item">
            {timeFrame[0]} - {timeFrame[1]}
          </p>
        </div>
        <p className="event-item">{content}</p>
        <div className="buttons"></div>
      </div>
    </div>
  );
}
