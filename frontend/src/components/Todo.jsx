import react from "react";
import api from "./../api";

export function Todo({ todo, onDelete, onEdit, getTodos }) {
  const setStatus = async (todo) => {
    try {
      const response = await api.put(
        `api/all/status/${todo.title}/${todo.item_type}`,
        { completed: !todo.completed }
      );

      if (response.status === 204) {
        console.log("Todo was edited successfully");
      } else {
        console.error("failed to edit the todo");
      }
    } catch (error) {
      console.error("Failed to set todo status", error);
    }
    getTodos(); 
  };

  return (
    <div className="todl-container">
      {/* <h3>{todo.title}</h3> */}

      <span
        style={{ textDecoration: todo.completed ? "line-through" : "none" }}
      >
        {todo.content}
      </span>

      <button
        className="delete-button"
        onClick={() => onDelete(todo.title, todo.item_type)}
      >
        Delete
      </button>
      <button
        className="edit-button"
        onClick={() => onEdit(todo.title, todo.item_type)}
      >
        Edit
      </button>
      <button className="edit-button" onClick={() => setStatus(todo)}>
        {todo.completed ? "Undo" : "Complete"}
      </button>
    </div>
  );
}
