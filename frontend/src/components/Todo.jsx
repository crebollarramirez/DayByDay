import react from "react";

export function Todo({ todo, onDelete, onEdit }) {
  return (
    <div className="todl-container">
      {/* <h3>{todo.title}</h3> */}
      <p className="todo-content">{todo.content}</p>
      <button className="delete-button" onClick={() => onDelete(todo.title, todo.item_type)}>
        Delete
      </button>
      <button className="edit-button" onClick={() => onEdit(todo.title, todo.item_type)}>
        Edit
      </button>
    </div>
  );
}
