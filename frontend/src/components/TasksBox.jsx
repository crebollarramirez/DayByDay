import React, { useEffect, useState } from "react";
import api from "../api";
import { Task } from "./Task";

export function TasksBox({getTasks, tasks}) {

  const deleteTask = (id) => {
    api.delete(`/api/tasks/delete/${id}/`).then((res) => {
      if (res.status === 204) alert("The Task was deleted");
      else alert("failed to delete note.");
      getTasks();
    });
  };

  return (
    <div className="tasks-container">
      <h2>Tasks</h2>
      {tasks.map((task) => (
        <Task task={task} onDelete={deleteTask} key={task.id} />
      ))}
    </div>
  );
}
