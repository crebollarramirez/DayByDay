import React, { useState } from "react";
import "../../styles/createMenuStyle.css";

export function CreateMenu() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [itemType, setItemType] = useState("TODO");
  const [scheduledDay, setScheduledDay] = useState("");
  const [frequency, setFrequency] = useState([]);

  const handleFrequencyChange = (e) => {
    const selectedOptions = Array.from(e.target.selectedOptions, option => option.value);
    setFrequency(selectedOptions); // Set the selected options as an array
  };

  const onSubmit = (e) => {
    e.preventDefault();
    console.log(title, content, itemType, scheduledDay, frequency);

    // handle form submission logic here
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

        {itemType === "TASK" && (
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

            <label htmlFor="scheduledDay">Scheduled Day</label>
            <input
              type="date"
              id="scheduledDay"
              name="scheduledDay"
              value={scheduledDay}
              onChange={(e) => setScheduledDay(e.target.value)}
              required
            />

            <label htmlFor="frequency">Frequency</label>
            <select
              name="frequency"
              id="frequency"
              value={frequency}
              onChange={handleFrequencyChange}
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
        <br />
        <input type="submit" value="Submit" />
      </form>
    </div>
  );
}
