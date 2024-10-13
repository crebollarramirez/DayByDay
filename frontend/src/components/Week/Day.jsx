import React from "react";
import "../../styles/dayStyle.css";
import { Event } from "./Event";

export function Day({ day, events, getWeek }) {
  return (
    <div className="day-container">
      <h3>{day}</h3>
      <div className="events-container">
        {Object.entries(events).map(([title, eventData]) => (
          <Event
            key={title}
            title={title}
            content={eventData.content}
            timeFrame={eventData.timeFrame}
            isCompleted={eventData.isCompleted}
            item_type={eventData.item_type}
            getWeek={getWeek}
          />

        ))}
      </div>
    </div>
  );
}
