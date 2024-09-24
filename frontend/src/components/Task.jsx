import react from "react";

export function Task({ task, onDelete }) {
  return (
    <div className="task-container">
      <p className="note-content">{task.content}</p>
      <button className="delete-button" onClick={() => onDelete(task.content)}>
        Delete
      </button>
    </div>
  );
}
