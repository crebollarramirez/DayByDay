import React, { useState } from "react";
import "../../styles/createMenuStyle.css";
import api from "../../api";

export function CreateMenu({ getTodos }) {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [itemType, setItemType] = useState("TODO");
  const [scheduledDay, setScheduledDay] = useState("");
  const [endDay, setEndDay] = useState("");
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

  const handleFrequencyChange = (e) => {
    const selectedOptions = Array.from(
      e.target.selectedOptions,
      (option) => option.value
    );
    setFrequency(selectedOptions); // Set the selected options as an array
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
        endFrequency: endDay,
      };
    } else if (item_type === "TASK") {
      item = {
        title: title,
        content: content,
        item_type: item_type,
        completed: false,
        timeFrame: timeFrame,
        date: formatDate(scheduledDay),
      };
    }

    // Log the item for debugging
    console.log(item);
    // setFrequency([]);
    // setScheduledDay("");

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
          <div className="form__group field">
            <textarea
              className="form__field"
              id="content"
              name="content"
              required
              value={content}
              onChange={(e) => setContent(e.target.value)}
            ></textarea>
            <label htmlFor="content" className="form__label">
              Content
            </label>
          </div>
        )}

        {(itemType === "TASK" || itemType === "FREQUENT") && (
          <>
            <div className="form__group field">
              <textarea
                className="form__field"
                placeholder="Title"
                name="title"
                id="title"
                required
                value={title}
                onChange={(e) => setTitle(e.target.value)}
              />
              <label htmlFor="title" className="form__label">
                Title
              </label>
            </div>
            <div className="form__group field">
              <textarea
                className="form__field"
                id="content"
                name="content"
                required
                value={content}
                onChange={(e) => setContent(e.target.value)}
              ></textarea>
              <label htmlFor="content" className="form__label">
                Content
              </label>
            </div>

            {/* Only show scheduledDay if frequency is not selected */}
            {frequency.length === 0 && (
              <div className="form__group field">
                <label htmlFor="scheduledDay" className="form__label">Scheduled Day</label>
                <input
                  className="form__field"
                  type="date"
                  id="scheduledDay"
                  name="scheduledDay"
                  value={scheduledDay}
                  onChange={(e) => setScheduledDay(e.target.value)}
                  required
                />
              </div>
            )}

            <div className="time-container">
              <div className="form__group field">
                <label htmlFor="timeFrom" className="form__label">
                  From:
                </label>
                <input
                  type="time"
                  id="timeFrom"
                  name="timeFrom"
                  className="form__field"
                  min="00:00"
                  max="24:00"
                  required
                  onChange={handleTimeFromChange}
                />
              </div>

              <div className="form__group field">
                <label htmlFor="timeTo" className="form__label">
                  To:
                </label>
                <input
                  type="time"
                  id="timeTo"
                  name="timeTo"
                  className="form__field"
                  min="00:00"
                  max="24:00"
                  onChange={handleTimeToChange}
                />
              </div>
            </div>

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
                  required
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

                <label htmlFor="endDay">Frequency End</label>
                <input
                  type="date"
                  id="endDay"
                  name="endDay"
                  value={endDay}
                  onChange={(e) => setEndDay(e.target.value)}
                  required
                />
              </>
            )}
          </>
        )}

        <br />
        <input type="submit" value="Submit" className="submit-button" />
      </form>
    </div>
  );
}
