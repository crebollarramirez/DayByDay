import React from "react";
import api from "../api";
import { useAppContext } from "../context/AppProvider";

export function Todo({ todo }) {
  const { setSelectedTodo } = useAppContext();

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
      console.log("Failed to set todo status", error);
    }
  };

  const onDelete = async () => {
    console.log("Deleting todo: ", todo);
    try{
      const response = await api.delete(`api/todos/delete/${todo.item_id}/${todo.item_type}`);
      if(response.status === 204){
        console.log("Todo was deleted successfully");
      }else{
        console.error("Failed to delete the todo");
      }

    }catch(error){
      console.log("Failed to delete the todo", error);
    }
  };

  const onEdit = async (content) => {
    console.log("Editing todo: ", todo);
    try {
      const response = await api.put(`api/todos/edit/${todo.item_id}/${todo.item_type}`, { content: content });
      if (response.status === 204) {
        console.log("Todo was edited successfully");
      } else {
        console.error("Failed to edit the todo");
      }
    } catch (error) {
      console.log("Failed to edit the todo", error);
    }
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
        <div className="w-1/4 flex flex-row gap-1">

          <button
            className="text-sandTan hover:text-nightBlue border border-sandTan hover:bg-sandTan focus:outline-none py-1 w-full rounded-lg transition duration-300 ease-in-out"
            onClick={() => setSelectedTodo(todo)}
          >
            Edit
          </button>
        </div>
      </div>
    </div>
  );
}
