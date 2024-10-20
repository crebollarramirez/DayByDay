import React, { useEffect, useState } from "react";
import { TodayTask } from "./TodayTask";
import api from "../../api";
import { RightSideBar } from "./RightSideBar";
import "../../styles/todayStyle.css";

export function Today({ toggleCreateMenu }) {
  const [today, setToday] = useState({});
  const [date, setDate] = useState("");

  const formattedDate = () => {
    const now = new Date();
  
    const month = (now.getMonth() + 1).toString().padStart(2, '0'); // Months are zero-based, so we add 1
    const day = now.getDate().toString().padStart(2, '0');
    const year = now.getFullYear();
  
    return `${month}-${day}-${year}`;
  };
  
  const getToday = () => {
    const todayDate = formattedDate();

    api
      .get(`./api/today/list/${todayDate}`)
      .then((res) => res.data)
      .then((data) => {
        setToday(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };

  const getFormattedDate = (date = new Date()) => {
    const day = date.getDate();
    const monthNames = [
      "January",
      "February",
      "March",
      "April",
      "May",
      "June",
      "July",
      "August",
      "September",
      "October",
      "November",
      "December",
    ];
    const month = monthNames[date.getMonth()];
    const year = date.getFullYear();

    const getDayWithSuffix = (day) => {
      if (day > 3 && day < 21) return day + "th"; // Special case for 11th to 20th
      switch (day % 10) {
        case 1:
          return day + "st";
        case 2:
          return day + "nd";
        case 3:
          return day + "rd";
        default:
          return day + "th";
      }
    };

    return `${getDayWithSuffix(day)} ${month} ${year}`;
  };

  useEffect(() => {
    getToday();
    setDate(getFormattedDate());
  }, []);

  return (
    <div className="today-container">
      <div className="top-container today-item">
        <h1>Hello! USER </h1>
        <h2>Today's Plan</h2>
      </div>

      <div className="todayBox today-item">
        <div className="todayLabel">
          <h1>Today</h1>
          <h2>{date}</h2>
        </div>

        <div className="addNewTask-container">
          <button onClick={toggleCreateMenu}>Add New</button>
        </div>
      </div>

      <div className="bottom-container today-item">
        <h1>Upcoming Events</h1>
        <div className="todayEvents">
          {Object.entries(today).map(([taskKey, task]) => (
            <TodayTask key={taskKey} task={task} getWeek={getToday} />
          ))}
        </div>
      </div>
    </div>
  );
}
