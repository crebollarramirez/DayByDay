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
      })
      .catch((err) => alert(err));
  };

  useEffect(() => {
    getWeek();
  }, []); // Empty dependency array to fetch data once on moun

  return (
    <div className="week-container">
      <h1>Week</h1>
      {Object.entries(weekData).map(([day, tasks]) => (
        <Day day={day} tasks={tasks} getWeek={getWeek} />
      ))}
    </div>
  );
}
