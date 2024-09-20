import React, { useEffect, useState } from "react";
import { Week } from "./Week";
import { Today } from "./Today";
import { Info } from "./Info";
import { Task } from "./components/Task";
// import "./style.css";
import api from "./api";

function App() {
  const [tasks, setTasks] = useState([]);
  const [content, setContent] = useState("");
  const [title, setTitle] = useState("");

  useEffect(() => {
    getTasks();
  }, []);

  const getTasks = () => {
    api
      .get("./api/tasks/")
      .then((res) => res.data)
      .then((data) => {
        setTasks(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };

  const deleteTask = (id) => {
    api.delete(`/api/tasks/delete/${id}/`).then((res) => {
      if (res.status === 204) alert("The Task was deleted");
      else alert("failed to delete note.");
      getTasks();
    });
  };

  const createTask = (e) => {
    e.preventDefault();
    api
      .post("/api/tasks/", { content, title })
      .then((res) => {
        if (res.status === 201) alert("Task created!");
        else alert("Failed to make Task.");
        getTasks();
      })
      .catch((err) => alert(err)); // we are getting this error when submitting task, maybe backend issue
  };

  return (
    <main>
      <h2>Tasks</h2>
      {tasks.map((task) => (
        <Task task={task} onDelete={deleteTask} key={task.id} />
      ))} 

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
            setTitle(e.target.value);
          }}
        ></textarea>
        <br />
        <input type="submit" value="Submit"></input>
      </form>
    </main>
  );
}

export default App;

// {/* <main>
//   <div className="grid-container">
//   <Week className="week grid-item"/>
//   <Today className="today grid-item"/>
//   <Info className="info grid-item"/>
// </div>
// </main> */}
