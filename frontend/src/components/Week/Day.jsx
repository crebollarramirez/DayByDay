import React from "react";
import { Task } from "./Task";

export function Day({ day, tasks }) {
    const isTasksEmpty = Object.keys(tasks).length === 0;

  console.log(tasks);
  return (
    <div className="day-container">
        <h2>{day}</h2>
        {
            isTasksEmpty ? (
                <p>No tasks for today</p>
            ) : (
                Object.entries(tasks).map(([taskKey, task]) => (
                    <Task key={taskKey} task={task}/>
              ))
            )
        }
        
    </div>
  );
}
