import React, { useEffect, useState } from "react";
import api from "./../../api";
import { Day } from "./Day";
import "../../styles/weekStyle.css";
import { TimeLine } from "./TimeLine";

export function Week() {
  // const [weekData, setWeekData] = useState({});

  // const getWeek = () => {
  //   api
  //     .get("./api/week/list/")
  //     .then((res) => res.data)
  //     .then((data) => {
  //       setWeekData(data);
  //     })
  //     .catch((err) => alert(err));
  // };
  
  // useEffect(() => {
  //   getWeek();
  // }, []); // Empty dependency array to fetch data once on moun

  const dummyEvents = [
    {
      title: "Team Meeting",
      content: "Discuss project updates and goals.",
      timeFrame: "10:00 AM - 11:00 AM",
    },
    {
      title: "Lunch Break",
      content: "Time to relax and enjoy your lunch.",
      timeFrame: "12:00 PM - 1:00 PM",
    },
    {
      title: "Client Call",
      content: "Call with the client to go over final deliverables.",
      timeFrame: "2:00 PM - 3:00 PM",
    },
    {
      title: "Code Review",
      content: "Review code submissions from the team.",
      timeFrame: "4:00 PM - 5:00 PM",
    },
  ];

  return (
    <div className="week-container">
      <TimeLine />
      <Day day={"9 Mon"} events={dummyEvents}/>
      <Day day={"10 Tues"}  />
      <Day day={"11 Thur"} />
      <Day day={"12 Fri"} />
      <Day day={"13 Sat"} />
      <Day day={"14 Sun"} />
    </div>
  );
}
