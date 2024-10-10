import React, { useEffect, useState } from "react";
import api from "./../../api";
import { Day } from "./Day";
import "../../styles/weekStyle.css";
import { TimeLine } from "./TimeLine";

export function Week() {
  const [weekData, setWeekData] = useState({});

  const getWeek = () => {
    api
      .get("./api/week/list/")
      .then((res) => res.data)
      .then((data) => {
        setWeekData(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };

  useEffect(() => {
    getWeek();
  }, []); // Empty dependency array to fetch data once on moun

  return (
    <div className="week-container">
      <TimeLine />
      {Object.entries(weekData).map(([day, events]) => (
        <Day key={day} day={day} events={events} />
      ))}
    </div>
  );
}
