import React from "react";

export function Day({day}){
    return (
        <div className="day-container">
            <h2>{day.name}</h2>
            <p>{}</p>
        </div>
    )
}