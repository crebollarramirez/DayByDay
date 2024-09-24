import React, { useState} from "react";
import api from "../api";

export function CreateTaskBlock({getTasks}) {
  const [content, setContent] = useState("");

  const createTask = (e) => {
    e.preventDefault();
    api
      .post("/api/todos/", { content })
      .then((res) => {
        if (res.status === 201) {
          alert("Task created!");
          getTasks(); // Call getTasks here to update the task list
        } else {
          alert("Failed to make Task.");
        }
      })
      .catch((err) => alert(err));
  };

  return (
    <div className="createTask-container">
      <h2>Create task</h2>
      <form onSubmit={createTask}>
        <label htmlFor="title">Content</label>
        <br />
        <textarea
          id="content"
          name="content"
          required
          value={content}
          onChange={(e) => {
            setContent(e.target.value);
          }}
        ></textarea>
        <br />
        <input type="submit" value="Submit"></input>
      </form>
    </div>
  );
}
