import react from "react"

export function Task({task, onDelete}){
    <div className="task-container">
        <p className="note-content">{task.content}</p>
        <button className="delete-button" onClick={() => onDelete(task.id)}>
        Delete
      </button>
    </div>
}