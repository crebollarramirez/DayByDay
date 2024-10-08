import React, { useState, useEffect } from "react";
import "../../styles/timeLineStyle.css"

export function TimeLine() {
  return (
    <div className="timeLine-container">
      <div className="timeMarker">9 AM</div>
      <div className="timeMarker">10 AM</div>
      <div className="timeMarker">11 AM</div>
      <div className="timeMarker">12 PM</div>
      <div className="timeMarker">1 PM</div>
      <div className="timeMarker">2 PM</div>
      <div className="timeMarker">3 PM</div>
      <div className="timeMarker">4 PM</div>
      <div className="timeMarker">5 PM</div>
      <div className="timeMarker">5 PM</div>
      <div className="timeMarker">5 PM</div>
      <div className="timeMarker">5 PM</div>
    </div>
  );
}
