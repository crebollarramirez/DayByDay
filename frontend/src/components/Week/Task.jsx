import React from "react";

export function Task({ taskKey, task }) {
  return (
    <div key={taskKey} className="task">
      <h3>{task.title}</h3>
      <p>{task.content}</p>
      <p>
        Time: {task.timeFrame[0]} - {task.timeFrame[1]}
      </p>
      <p>Completed: {task.completed ? "Yes" : "No"}</p>
    </div>
  );
}
