import React from "react";
import api from "../api";

export function Todo({ todo }) {
  const setStatus = async (todo) => {
    try {
      const response = await api.put(
        `api/all/status/${todo.item_id}/${todo.item_type}`,
        { completed: !todo.completed }
      );

      if (response.status === 204) {
        console.log("Todo was edited successfully");
      } else {
        console.error("Failed to edit the todo");
      }
    } catch (error) {
      console.error("Failed to set todo status", error);
    }
    // getTodos();
  };

  return (
    <div className="w-full flex flex-col p-3 rounded-lg bg-nightBlue gap-2">
      <div className="w-full flex flex-row items-center justify-start gap-2">
        <input
          type="checkbox"
          // checked={todo.completed}
          onChange={() => setStatus(todo)} // Toggle the completion status
          className="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600"
        />
        <span
          style={{ textDecoration: todo.completed ? "line-through" : "none" }}
        >
          <p className="text-dustyWhite">{todo.content}</p>
        </span>
      </div>

      <div className="w-full flex justify-end items-center">
        <div className="w-1/2 flex flex-row gap-1">
          <button
            className="text-sandTan hover:text-nightBlue border border-sandTan hover:bg-sandTan focus:outline-none py-1 w-full rounded-lg transition duration-300 ease-in-out"
            onClick={() => onDelete(todo.item_id, todo.item_type)}
          >
            Delete
          </button>
          <button
            className="text-sandTan hover:text-nightBlue border border-sandTan hover:bg-sandTan focus:outline-none py-1 w-full rounded-lg transition duration-300 ease-in-out"
            onClick={() => onEdit(todo.item_id, todo.item_type)}
          >
            Edit
          </button>
        </div>
      </div>
    </div>
  );
}
