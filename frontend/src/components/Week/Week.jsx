import React, { useEffect, useState } from "react";
import api from "./../../api";
import { Day } from "./Day";

export function Week() {
  const [weekData, setWeekData] = useState({});

  const getWeek = () => {
    api
      .get("./api/week/list/")
      .then((res) => res.data)
      .then((data) => {
        setWeekData(data);
        console.log("This is the week");
        console.log(data);
      })
      .catch((err) => alert(err));
  };

  useEffect(() => {
    getWeek();
  }, []); // Empty dependency array to fetch data once on moun

  console.log(weekData);
  if (!weekData || typeof weekData !== "object") {
    return <div>No week data available</div>;
  }

  return (
    <div className="week-container">
      <h1>Week</h1>
      {Object.entries(weekData).map(([day, tasks]) => (
        <Day day={day} tasks={tasks}/>
      ))}
    </div>
  );
}
