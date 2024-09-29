import React, { useEffect, useState } from "react";
import { Task } from "./Week/Task";
import api from "../api";

export function Today({ className }) {
  const [today, setToday] = useState({});

  const getToday = () => {
    api
      .get("./api/today/list/")
      .then((res) => res.data)
      .then((data) => {
        setToday(data);
        console.log("this is today");
        console.log(data);
      })
      .catch((err) => alert(err));
  };

  useEffect(() => {
    getToday();
  }, []);
  console.log("this is todaaaaaaaa");
  console.log(today);
  return (
    <div className={className}>
      <h1>Today</h1>
      {Object.entries(today).map(([taskKey, task]) => (
        <Task key={taskKey} task={task} />
      ))}
    </div>
  );
}
