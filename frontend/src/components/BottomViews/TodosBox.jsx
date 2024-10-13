import React, { useEffect, useState } from "react";
import api from "../../api";
import { Todo } from "./Todo";
import '../../styles/todosBoxStyle.css';

export function TodosBox({getTodos, todos}) {

  // Function to delete a task
  const deleteTodo = async (title, item_type) => {

    try {
      const response = await api.delete(
        `api/todos/delete/${title}/${item_type}`
      );

      if (response.status === 204) {
        console.log("Task deleted successfully");
        // Optionally refresh tasks or update state here
      } else {
        console.error("Failed to delete the task");
      }
    } catch (error) {
      console.error("Failed to delete the task", error);
    }
    getTodos();
  };

  const editTodo = async (title, item_type, newData = "edited") => {
    try {
      const response = await api.put(`api/todos/edit/${title}/${item_type}`, {
        newData,
      });

      if (response.status === 204) {
        console.log("Todo was edited successfully");
      } else {
        console.error("failed to edit the todo");
      }
    } catch (error) {
      console.error("Failed to edit the todo", error);
    }
    getTodos();
  };

  return (
    <div className="todos-container">
      <h2>Todos</h2>
      {todos.map((todo) => (
        <Todo
          todo={todo}
          onDelete={deleteTodo}
          onEdit={editTodo}
          key={todo.title}
          getTodos={getTodos}
        />
      ))}
    </div>
  );
}
