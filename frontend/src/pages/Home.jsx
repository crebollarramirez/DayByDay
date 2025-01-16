import React, { useState, useEffect } from "react";
import api from "../api";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import timeGridPlugin from "@fullcalendar/timegrid";

function Home() {
  const [todos, setTodos] = useState([]);
  const [isCreateMenuVisible, setIsCreateMenuVisible] = useState(false); // State for CreateMenu visibility
  const [username, setUsername] = useState("User");

  const getTodos = () => {
    const date = getFormattedDate();

    api
      .get(`./api/todos/${date}`)
      .then((res) => res.data)
      .then((data) => {
        setTodos(data);
        console.log("THIS IS THE TODOS: ");
        console.log(data);
      })
      .catch((err) => alert(err));
  };

  const getUserName = () => {
    api
      .get("./api/username/")
      .then((res) => res.data)
      .then((data) => {
        setUsername(data);
        console.log(data);
      })
      .catch((err) => alert(err));
  };

  const toggleCreateMenu = () => {
    setIsCreateMenuVisible(!isCreateMenuVisible); // Toggle visibility
  };

  // useEffect(() => {
  //   getTodos();
  //   getUserName();
  // }, []);

  const events = [{ title: "Meeting", start: new Date() }];

  function renderEventContent(eventInfo) {
    return (
      <>
        <b>{eventInfo.timeText}</b>
        <i>{eventInfo.event.title}</i>
      </>
    );
  }

  const handleDateClick = (arg) => {
    alert(arg.dateStr);
  };

  return (
    <div className="flex h-screen w-screen flex items-center justify-center flex-col bg-nightBlue">
      <div className="">
        <h1 className="text-4xl text-dustyWhite">Welcome {username} !</h1>
      </div>
      <div className="w-[50%] bg-white shadow-lg rounded-lg p-4">
        <FullCalendar
          plugins={[dayGridPlugin, timeGridPlugin, interactionPlugin]}
          initialView="dayGridMonth"
          weekends={true}
          dateClick={(e) => handleDateClick(e)}
          headerToolbar={{
            start: "today prev,next", // will normally be on the left. if RTL, will be on the right
            center: "title",
            end: "dayGridMonth,timeGridWeek,timeGridDay", // will normally be on the right. if RTL, will be on the left
          }}
          events={[
            { title: "event 1", date: "2021-05-07" },
            { title: "event 2", date: "2021-05-17" }
          ]}
          eventContent={renderEventContent}
        />
      </div>
    </div>
  );
}

export default Home;
