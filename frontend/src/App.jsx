import React, { useEffect, useState } from "react";
import { Week } from "./Week";
import { Today } from "./Today";
import { Info } from "./Info";
import { Task } from "./components/Task";
import { TasksBox } from "./components/TasksBox";
// import "./style.css";
import api from "./api";
import { CreateTaskBlock } from "./components/CreateTaskBlock";

function App() {
  const [tasks, setTasks] = useState([]);

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

  // const deleteAllTasks = () => {
  //   api
  //     .delete("/api/tasks/delete_all/") // Update the URL to your endpoint
  //     .then((res) => {
  //       if (res.status === 204) {
  //         alert("All tasks deleted successfully!");
  //         // Optionally, call getTasks to refresh the task list
  //         // getTasks();
  //       } else {
  //         alert("Failed to delete tasks.");
  //       }
  //     })
  //     .catch((err) => {
  //       console.error(err);
  //       alert("An error occurred while deleting tasks.");
  //     });
  //     getTasks();
  // };

  return (
    <main>
      <TasksBox getTasks={getTasks} tasks={tasks} />
      <CreateTaskBlock getTasks={getTasks} />
      {/* <button onClick={deleteAllTasks()}>Delete All</button> */}
    </main>
  );
}

export default App;
