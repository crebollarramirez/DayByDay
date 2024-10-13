import React, { useState } from "react";
import "../../styles/createMenuStyle.css";
import api from "../../api";

export function CreateMenu({ getTodos }) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [itemType, setItemType] = useState("TODO");
  const [scheduledDay, setScheduledDay] = useState("");
  const [frequency, setFrequency] = useState([]);
  const [timeFrame, setTimeFrame] = useState({ from: "", to: "" });

  // handle form submission logic here

  // api
  // .post("/api/todos/", item)
  // .then((res) => {
  //   if (res.status === 201) {
  //     alert("Todo created!");
  //     getTodos(); // Call getTasks here to update the task list
  //   } else {
  //     alert("Failed to make Todo.");
  //   }
  // })
  // .catch((err) => alert(err));

  const handleTimeFromChange = (e) => {
    setTimeFrame((prevTimeFrame) => ({
      ...prevTimeFrame,
      from: e.target.value,
    }));
  };

  const handleTimeToChange = (e) => {
    setTimeFrame((prevTimeFrame) => ({
      ...prevTimeFrame,
      to: e.target.value,
    }));
  };

  const handleFrequencyChange = (e) => {
    const selectedOptions = Array.from(
      e.target.selectedOptions,
      (option) => option.value
    );
    setFrequency(selectedOptions); // Set the selected options as an array
  };

  const createTodo = (e) => {
    const toDoInfo = {
      title: content,
      content: content,
      item_type: "TODO",
      completed: false,
    };

    e.preventDefault();
  };

  const onSubmit = (e) => {
    e.preventDefault();

    let item = {};
    var item_type = "TODO";

    // Prioritize "FREQUENT" if frequency is selected

    if (frequency.length !== 0) {
      console.log("this is running");
      item_type = "FREQUENT";
    } else if (scheduledDay !== "") {
      // Only set to "TASK" if frequency is empty and scheduledDay is provided
      console.log("This is also running");
      item_type = "TASK";
    }

    if (item_type === "TODO") {
      item = {
        title: content,
        content: content,
        item_type: item_type,
        completed: false,
      };
    } else if (item_type === "FREQUENT") {
      item = {
        title: title,
        content: content,
        item_type: item_type,
        completed: false,
        frequency: frequency, // Make sure frequency is included
        timeFrame: timeFrame,
      };
    } else if (item_type === "TASK") {
      item = {
        title: title,
        content: content,
        item_type: item_type,
        completed: false,
        timeFrame: timeFrame,
        date: scheduledDay,
      };
    }

    // Log the item for debugging
    console.log(item);
    console.log(frequency);
    setTimeFrame({ from: "", to: "" });
    setFrequency([]);
    setScheduledDay("");

    // Form submission logic...
  };

  return (
    <div className="create-container">
      <h2>Create Task</h2>
      <form onSubmit={onSubmit}>
        <label htmlFor="item_type">Task Type:</label>
        <select
          name="item_type"
          id="item_type"
          value={itemType}
          onChange={(e) => setItemType(e.target.value)}
        >
          <option value="TODO">Todo</option>
          <option value="TASK">Scheduled Task</option>
        </select>

        {itemType === "TODO" && (
          <>
            <label htmlFor="content">Content</label>
            <textarea
              id="content"
              name="content"
              required
              value={content}
              onChange={(e) => setContent(e.target.value)}
            ></textarea>
          </>
        )}

        {(itemType === "TASK" || itemType === "FREQUENT") && (
          <>
            <label htmlFor="title">Title</label>
            <textarea
              id="title"
              name="title"
              required
              value={title}
              onChange={(e) => setTitle(e.target.value)}
            ></textarea>

            <label htmlFor="content">Content</label>
            <textarea
              id="content"
              name="content"
              required
              value={content}
              onChange={(e) => setContent(e.target.value)}
            ></textarea>

            {/* Only show scheduledDay if frequency is not selected */}
            {frequency.length === 0 && (
              <>
                <label htmlFor="scheduledDay">Scheduled Day</label>
                <input
                  type="date"
                  id="scheduledDay"
                  name="scheduledDay"
                  value={scheduledDay}
                  onChange={(e) => setScheduledDay(e.target.value)}
                />
              </>
            )}

            <label htmlFor="timeFrom">From:</label>
            <input
              type="time"
              id="timeFrom"
              name="timeFrom"
              min="00:00"
              max="24:00"
              onChange={handleTimeFromChange}
            />

            <label htmlFor="timeTo">To:</label>
            <input
              type="time"
              id="timeTo"
              name="timeTo"
              min="00:00"
              max="24:00"
              onChange={handleTimeToChange}
            />

            {/* Only show frequency if scheduledDay is not filled */}
            {scheduledDay === "" && (
              <>
                <label htmlFor="frequency">Frequency</label>
                <select
                  name="frequency"
                  id="frequency"
                  value={frequency}
                  onChange={(e) => handleFrequencyChange(e)}
                  multiple
                >
                  <option value="Monday">Monday</option>
                  <option value="Tuesday">Tuesday</option>
                  <option value="Wednesday">Wednesday</option>
                  <option value="Thursday">Thursday</option>
                  <option value="Friday">Friday</option>
                  <option value="Saturday">Saturday</option>
                  <option value="Sunday">Sunday</option>
                  <option value="Everyday">Everyday</option>
                  <option value="Biweekly">Biweekly</option>
                  <option value="Monthly">Monthly</option>
                  <option value="Yearly">Yearly</option>
                </select>
              </>
            )}
          </>
        )}

        <br />
        <input type="submit" value="Submit" />
      </form>
    </div>
  );
}
