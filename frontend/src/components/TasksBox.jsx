import React, { useEffect, useState } from "react";
import api from "../api";
import { Task } from "./Task";

export function TasksBox({getTasks, tasks}) {

  // Function to delete a task
  const deleteTask = async (taskId) => {
    try {
        const response = await api.delete(`api/todos/${encodeURIComponent(taskId)}/`);

        if (response.status === 204) {
            console.log('Task deleted successfully');
            // Optionally refresh tasks or update state here
        } else {
            console.error('Failed to delete the task');
        }
    } catch (error) {
        console.error('Failed to delete the task', error);
    }
    getTasks();
};

  return (
    <div className="tasks-container">
      <h2>Tasks</h2>
      {tasks.map((task) => (
        <Task task={task} onDelete={deleteTask} key={task.content} />
      ))}
    </div>
  );
}
