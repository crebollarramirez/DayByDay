import React, { useState } from "react";
import api from "../api";

export function CreateMenu({ getTodos }) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [itemType, setItemType] = useState("TODO");
  const [scheduledDay, setScheduledDay] = useState("");
  const [frequency, setFrequency] = useState([]);
  const [timeFrame, setTimeFrame] = useState(["", ""]);

  const handleTimeFromChange = (e) => {
    setTimeFrame([e.target.value, timeFrame[1]]); // Set the "from" time (first element)
  };

  const handleTimeToChange = (e) => {
    setTimeFrame([timeFrame[0], e.target.value]); // Set the "to" time (second element)
  };

  const formatDate = (date) => {
    const [year, month, day] = date.split("-"); // Split into components
    return `${month}-${day}-${year}`;
  };

  const onSubmit = (e) => {
    e.preventDefault();

    var item = {};

    if (itemType === "TODO") {
      item = {
        content: content,
        item_type: "TODO",
        date: formatDate(scheduledDay),
      };
    } else if (itemType === "TASK") {
      item = {
        title: title,
        content: content,
        item_type: "TASK",
        timeFrame: timeFrame,
        date: formatDate(scheduledDay),
      };
    }

    console.log(item);
    setScheduledDay("");

    api
      .post("/api/tasks/", item)
      .then((res) => {
        if (res.status === 201) {
          alert("Task created!");
          getTodos(); // Call getTasks here to update the task list
        } else {
          alert("Failed to make Todo.");
        }
      })
      .catch((err) => alert(err));

    getTodos();
  };

  return (
    <div className="w-full p-6 bg-nightBlue rounded-lg shadow-lg">
      <h2 className="text-2xl font-bold text-dustyWhite">Create Task</h2>
      <form onSubmit={onSubmit} className="space-y-4">
        <div className="mb-4">
          <label
            htmlFor="item_type"
            className="block text-nightBlue font-semibold"
          >
            Task Type:
          </label>
          <select
            name="item_type"
            id="item_type"
            value={itemType}
            onChange={(e) => setItemType(e.target.value)}
            className="w-full p-2 border border-sandTan rounded-md focus:outline-none focus:ring-2 focus:ring-nightBlue bg-dustyWhite"
          >
            <option value="TODO">Todo</option>
            <option value="TASK">Scheduled Task</option>
          </select>
        </div>

        {itemType === "TODO" && (
          <div className="space-y-4">
            <div>
              <textarea
                className="w-full p-3 border border-sandTan rounded-md focus:outline-none focus:ring-2 focus:ring-nightBlue bg-dustyWhite resize-none"
                id="content"
                name="content"
                required
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Content"
                rows="4"
              ></textarea>
            </div>
            <div>
              <label
                htmlFor="scheduledDay"
                className="block text-dustyWhite font-semibold mb-2"
              >
                Scheduled Day
              </label>
              <input
                className="w-full p-2 border border-sandTan rounded-md focus:outline-none focus:ring-2 focus:ring-nightBlue bg-dustyWhite"
                type="date"
                id="scheduledDay"
                name="scheduledDay"
                value={scheduledDay}
                onChange={(e) => setScheduledDay(e.target.value)}
                required
              />
            </div>
          </div>
        )}

        {(itemType === "TASK" || itemType === "FREQUENT") && (
          <div className="space-y-4">
            <div>
              <textarea
                className="w-full p-3 border border-sandTan rounded-md focus:outline-none focus:ring-2 focus:ring-nightBlue bg-dustyWhite"
                placeholder="Title"
                name="title"
                id="title"
                required
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                rows="2"
              />
            </div>
            <div>
              <textarea
                className="w-full p-3 border border-sandTan rounded-md focus:outline-none focus:ring-2 focus:ring-nightBlue bg-dustyWhite"
                id="content"
                name="content"
                required
                value={content}
                onChange={(e) => setContent(e.target.value)}
                placeholder="Content"
                rows="4"
              ></textarea>
            </div>

            <div>
              <label
                htmlFor="scheduledDay"
                className="block text-dustyWhite font-semibold mb-2"
              >
                Scheduled Day
              </label>
              <input
                className="w-full p-2 border border-sandTan rounded-md focus:outline-none focus:ring-2 focus:ring-nightBlue bg-dustyWhite"
                type="date"
                id="scheduledDay"
                name="scheduledDay"
                value={scheduledDay}
                onChange={(e) => setScheduledDay(e.target.value)}
                required
              />
            </div>

            <div className="grid grid-cols-2 gap-4">
              <div>
                <label
                  htmlFor="timeFrom"
                  className="block text-dustyWhite font-semibold mb-2"
                >
                  From:
                </label>
                <input
                  type="time"
                  id="timeFrom"
                  name="timeFrom"
                  className="w-full p-2 border border-sandTan rounded-md focus:outline-none focus:ring-2 focus:ring-nightBlue bg-dustyWhite"
                  min="00:00"
                  max="24:00"
                  required
                  onChange={handleTimeFromChange}
                />
              </div>

              <div>
                <label
                  htmlFor="timeTo"
                  className="block text-dustyWhite font-semibold mb-2"
                >
                  To:
                </label>
                <input
                  type="time"
                  id="timeTo"
                  name="timeTo"
                  className="w-full p-2 border border-sandTan rounded-md focus:outline-none focus:ring-2 focus:ring-nightBlue bg-dustyWhite"
                  min="00:00"
                  max="24:00"
                  onChange={handleTimeToChange}
                />
              </div>
            </div>
          </div>
        )}

        <button
          type="submit"
          className="w-full bg-sandTan hover:bg-sanTanShadow text-nightBlue font-bold py-2 px-4 rounded-md transition duration-300 ease-in-out"
        >
          Submit
        </button>
      </form>
    </div>
  );
}
