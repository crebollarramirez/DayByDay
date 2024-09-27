import React, { useState} from "react";
import api from "../api";

export function CreateTodoBlock({getTodos}) {
  const [content, setContent] = useState("");

  const createTodo = (e) => {
    const toDoInfo = {
      title: content,
      content: content,
      item_type: "TODO",
      completed: false
    }
    
    e.preventDefault();
    api
      .post('/api/todos/', toDoInfo)
      .then((res) => {
        if (res.status === 201) {
          alert("Todo created!");
          getTodos(); // Call getTasks here to update the task list
        } else {
          alert("Failed to make Todo.");
        }
      })
      .catch((err) => alert(err));
  };

  return (
    <div className="createTodo-container">
      <h2>Create Todo</h2>
      <form onSubmit={createTodo}>
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
