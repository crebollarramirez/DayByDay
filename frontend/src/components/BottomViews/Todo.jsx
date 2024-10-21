import React from "react";
import api from "../../api";
import "../../styles/todoStyle.css";

export function Todo({ todo, onDelete, onEdit, getTodos }) {
  const setStatus = async (todo) => {
    try {
      const response = await api.put(
        `api/all/status/${todo.item_id}/${todo.item_type}`,
        { completed: !todo.completed }
      );

      if (response.status === 204) {
        console.log("Todo was edited successfully");
      } else {
        console.error("Failed to edit the todo");
      }
    } catch (error) {
      console.error("Failed to set todo status", error);
    }
    getTodos();
  };

  return (
    <div className="todo-container">
      <div className="content">
        <input
          type="checkbox"
          checked={todo.completed}
          onChange={() => setStatus(todo)} // Toggle the completion status
          className="checkbox" // Optional: Add a class for styling
        />
        <span
          style={{ textDecoration: todo.completed ? "line-through" : "none" }}
        >
          <p>{todo.content}</p>
        </span>
      </div>

      <div className="buttons">
        <button
          className="delete-button"
          onClick={() => onDelete(todo.item_id, todo.item_type)}
        >
          Delete
        </button>
        <button
          className="edit-button"
          onClick={() => onEdit(todo.item_id, todo.item_type)}
        >
          Edit
        </button>
      </div>
    </div>
  );
}
