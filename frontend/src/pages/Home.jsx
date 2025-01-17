import React, { useState, useEffect } from "react";
import api from "../api";
import FullCalendar from "@fullcalendar/react";
import dayGridPlugin from "@fullcalendar/daygrid";
import interactionPlugin from "@fullcalendar/interaction";
import timeGridPlugin from "@fullcalendar/timegrid";
import QuoteOfTheDay from "../components/QuoteOfTheDay";
import { TodosBox } from "../components/TodosBox";
import { CreateMenu } from "../components/CreateMenu";
import { AIChat } from "../components/AIChat";

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

  const events = [{ title: "Meeting", start: new Date()}];

  function renderEventContent(eventInfo) {
    return (
      <div className="flex items-center">
        <b className="mr-2">{eventInfo.timeText}</b>
        <i>{eventInfo.event.title}</i>
      </div>
    );
  }

  const handleDateClick = (arg) => {
    alert(arg.dateStr);
  };

  const handleEventClick = (clickInfo) => {
    alert(`Event: ${clickInfo.event.title}`);
  };

  return (
    <div className="h-full w-full lg:grid lg:grid-cols-6 lg:gap-0 lg:grid-rows-6 lg:gap-x-2 p-4 md:flex md:flex-col md:gap-4 md:h-screen">
      <div className="col-start-2 col-end-5 row-start-1 row-end-6 h-full w-full flex flex-col items-center justify-center gap-4 md:order-2">
        <h1 className="text-4xl text-dustyWhite">Welcome {username}!</h1>
        <div className="w-full rounded-lg p-4 bg-gradient-to-b from-sandTan to-sanTanShadow">
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
            events={events}
            eventContent={renderEventContent}
            eventClick={handleEventClick} // Handle event clicks
          />
        </div>
      </div>
      <div className="col-start-5 col-end-7 row-span-full h-full w-full flex flex-col items-center justify-center rounded-lg md:order-4 md:gap-3">
        <CreateMenu />
        <AIChat />
      </div>
      <div className="col-start-1 col-end-2 row-span-full h-full w-full flex flex-col items-center justify-center bg-gradient-to-b from-sandTan to-sanTanShadow rounded-lg md:order-3">
        <TodosBox />
      </div>
      <div className="col-start-2 col-end-5 row-span-6 h-full w-full flex flex-col items-center justify-center bg-gradient-to-b from-sandTan to-sanTanShadow rounded-lg md:order-1">
        <QuoteOfTheDay />
      </div>
    </div>
  );
}

export default Home;
