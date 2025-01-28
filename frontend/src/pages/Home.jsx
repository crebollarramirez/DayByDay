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
import { Task } from "../components/Task";
import { useAppContext } from "../context/AppProvider";

function Home() {
  const { selectedTask, setSelectedTask } = useAppContext();
  const [todos, setTodos] = useState([]);
  const [isCreateMenuVisible, setIsCreateMenuVisible] = useState(false);
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
    setIsCreateMenuVisible(!isCreateMenuVisible);
  };

  const events = [
    {
      item_id: "asdfasdf334",
      title: "Meeting",
      content:
        "Lorem ipsum dolor sit amet consectetur adipisicing elit. Architecto, autem similique. Corrupti, similique. Maxime quod excepturi magnam consequatur aut iste provident rem est eius pariatur facere, omnis dicta rerum saepe mollitia accusantium tempora quas itaque atque, ea, error ipsa id consectetur? Harum laborum quae a pariatur itaque officia et ea eos, nemo similique nam dicta sunt deserunt autem nihil aliquid ut porro perspiciatis nobis provident? Fugit velit vitae saepe veniam similique et vero illo voluptatem minima numquam amet laborum, ipsum illum minus assumenda fuga dignissimos, nesciunt harum! Illum animi cumque in accusamus nulla minima rem et molestias eligendi! Pariatur, harum.",
      start: "2025-01-28T10:00:00", // Start time
      end: "2025-01-28T15:00:00", // End time
      isCompleted: false,
    },
  ];

  function renderEventContent(eventInfo) {
    return (
      <div className="flex items-center gap-1 w-full border h-full text-nightBlueShadow flex-ro">
        <input type="checkbox" className="" />
        <b className="sm:text-xs">{eventInfo.timeText}</b>
        <i className="sm:text-xs">{eventInfo.event.title}</i>
      </div>
    );
  }

  const handleDateClick = (arg) => {
    alert(arg.dateStr);
  };

  const handleEventClick = (clickInfo) => {
    setSelectedTask({
      title: clickInfo.event.title,
      content: clickInfo.event.extendedProps.content,
      timeFrame: clickInfo.event.extendedProps.timeFrame,
      item_id: clickInfo.event.extendedProps.item_id,
      date: clickInfo.event.extendedProps.date,
    });
  };

  useEffect(() => {
    // getTodos();
    // getUserName();
  }, []);

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
              start: "today prev,next",
              center: "title",
              end: "dayGridMonth,timeGridWeek,timeGridDay",
            }}
            events={events}
            eventContent={renderEventContent}
            eventClick={handleEventClick}
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

      {selectedTask && <Task task={selectedTask} />}
    </div>
  );
}

export default Home;
