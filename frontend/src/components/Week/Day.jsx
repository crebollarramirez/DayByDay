import React from "react";
import "../../styles/dayStyle.css";
import { Event } from "./Event";

export function Day({ day, events }) {
  return (
    <div className="day-container">
      <h3>{day}</h3>
      <div className="events-container">
        {events && events.length > 0 ? (
          events.map((event, index) => (
            <Event 
              key={index} 
              title={event.title} 
              content={event.content} 
              timeFrame={event.timeFrame} 
            />
          ))
        ) : (
          <p>No events scheduled.</p> // Display a message if there are no events
        )}
      </div>
    </div>
  );
}
