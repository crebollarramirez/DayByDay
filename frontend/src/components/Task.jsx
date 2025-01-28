import React, { useState } from "react";
import { useAppContext } from "../context/AppProvider";
import api from "../api";

export const Task = ({ task }) => {
  const { setSelectedTask } = useAppContext();
  const [editing, setEditing] = useState(false);
  const [title, setTitle] = useState(null);
  const [content, setContent] = useState(null);
  const [date, setDate] = useState(null);
  const [isCompleted, setIsCompleted] = useState(null);

  const editTask = async (
    title = null,
    content = null,
    isCompleted = null,
    date = null
  ) => {
    const payload = {};
    if (title !== null) payload.title = title;
    if (content !== null) payload.content = content;
    if (isCompleted !== null) payload.isCompleted = isCompleted;
    if (date !== null) payload.date = date;

    console.log(payload);
    setTitle(null);
    setContent(null);
    setDate(null);
    setIsCompleted(null);

    // try {
    //   api.patch("./api/tasks/", { payload });
    // } catch (error) {
    //   console.log(error);
    // }
  };

  const deleteTask = async (task_id) => {
    // try {
    //   api.delete(`./api/tasks/${task_id}`);
    // } catch (error) {
    //   console.log(error);
    // }
    console.log("deleting task: ", task_id);
    setSelectedTask(null);
  };

  return (
    <div className="flex items-center justify-start flex-col fixed lg:w-1/4 lg:h-1/3 bg-nightBlueShadow rounded-lg shadow-lg p-4 top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 md:w-1/2 md:h-1/3 sm:w-1/2 sm:h-1/3 z-50">
      <button
        className="absolute top-2 right-2 py-1 text-sandTan hover:text-nightBlue border border-sandTan hover:bg-sandTan focus:outline-none rounded-lg transition duration-300 ease-in-out sm:px-3 sm:py-1"
        onClick={() => {
          setSelectedTask(null);
          console.log("exiting");
        }}
      >
        &times;
      </button>

      {!editing ? (
        <div className="w-full h-full flex flex-col gap-2">
          <div className="w-full h-[90%] flex justify-start items-center flex-col gap-4">
            <div className="flex w-full items-center justify-center gap-2">
              <input
                type="checkbox"
                checked={task.isCompleted}
                onChange={(e) => setIsCompleted(e.target.checked)}
                className="h-5 w-5 "
              />
              <h3 className="text-sandTan text-4xl">{task.title}</h3>
            </div>

            <p className="text-dustyWhite text-2xl text-start w-full overflow-y-auto">
              {task.content}
            </p>
          </div>
          <div className="h-[10%] w-full flex flex-row items-center gap-1">
            <button
              className="w-[50%] h-full text-sandTan hover:text-nightBlue border border-sandTan hover:bg-sandTan focus:outline-none rounded-lg transition duration-300 ease-in-out"
              onClick={() => setEditing(true)}
            >
              Edit
            </button>
            <button
              className="w-[50%] h-full text-sandTan hover:text-nightBlue border border-sandTan hover:bg-sandTan focus:outline-none rounded-lg transition duration-300 ease-in-out"
              onClick={() => deleteTask(task.item_id)}
            >
              Delete
            </button>
          </div>
        </div>
      ) : (
        <div className="w-full h-full flex flex-col gap-2">
          <div className="h-[90%] w-full flex flex-col gap-2">
            <label
              htmlFor="Title"
              className="block text-dustyWhite font-semibold"
            >
              Title:
            </label>
            <input
              type="text"
              className="w-full h-1/7 p-2 first-line:p-2 text-nightBlue border border-sandTan bg-dustyWhite rounded-lg"
              placeholder={task.title}
              onChange={(e) => setTitle(e.target.value)}
            />
            <label
              htmlFor="Content"
              className="block text-dustyWhite font-semibold"
            >
              Content:
            </label>
            <textarea
              className="w-full flex-grow p-2 text-nightBlue border border-sandTan rounded-lg bg-dustyWhite resize-none"
              placeholder={task.content}
              onChange={(e) => setContent(e.target.value)}
            />

            <label
              htmlFor="date"
              className="block text-dustyWhite font-semibold"
            >
              Date:
            </label>
            <input
              type="date"
              className="w-full h-1/7 p-2 text-nightBlue border border-sandTan bg-dustyWhite rounded-lg"
              placeholder={task.date}
              onChange={(e) => setDate(e.target.value)}
            />
          </div>

          <div className="h-[10%] w-full flex flex-row items-center gap-1">
            <button
              className="w-full h-full text-sandTan hover:text-nightBlue border border-sandTan hover:bg-sandTan focus:outline-none rounded-lg transition duration-300 ease-in-out"
              onClick={() => {
                setEditing(false);
                editTask(title, content, isCompleted, date);
              }}
            >
              Update
            </button>
          </div>
        </div>
      )}
    </div>
  );
};
