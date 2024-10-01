import React from "react";
import api from "../api";

export function Task({ taskKey, task, getWeek }) {
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
    try{
      const response = await api.delete(
        `api/tasks/delete/${title}/${item_type}`
      );

    }catch(error){
      console.log("Failed to delete the task");
    };
    getWeek();
  }
  return (
    <div key={taskKey} className="task">
      <h3>{task.title}</h3>
      <p>{task.content}</p>
      <p>
        Time: {task.timeFrame[0]} - {task.timeFrame[1]}
      </p>
      <p>Completed: {task.completed ? "Yes" : "No"}</p>

      <button className="edit-button" onClick={() => setStatus(task)}>
        {task.completed ? "Undo" : "Complete"}
      </button>
      <button onClick={() => onDelete(task.title, task.item_type)}>Delete!</button>
    </div>
  );
}
