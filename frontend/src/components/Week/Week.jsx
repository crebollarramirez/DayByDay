import React, { useEffect, useState } from "react";
import api from "./../../api";
import { Day } from "./Day";
import "../../styles/weekStyle.css";
import { TimeLine } from "./TimeLine";

export function Week() {
  const [weekData, setWeekData] = useState({});

  const getFormattedDate = () => {
    const now = new Date();
  
    const month = (now.getMonth() + 1).toString().padStart(2, '0'); // Months are zero-based, so we add 1
    const day = now.getDate().toString().padStart(2, '0');
    const year = now.getFullYear();
  
    return `${month}-${day}-${year}`;
  };

  const getWeek = () => {
    const date = getFormattedDate()

    api
      .get(`./api/week/list/${date}`)
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
        <Day key={day} day={day} events={events} getWeek={getWeek} />
      ))}
    </div>
  );
}
