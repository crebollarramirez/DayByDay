import React, { useEffect, useState } from "react";
import { TasksBox } from "./components/TasksBox";
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

  return (
    <main>
      <TasksBox getTasks={getTasks} tasks={tasks} />
      <CreateTaskBlock getTasks={getTasks} />
    </main>
  );
}

export default App;
