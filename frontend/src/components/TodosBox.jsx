import React, { useEffect, useState } from "react";
import api from "../api";
import { Todo } from "./Todo";

export function TodosBox() {
  const todos = [
    {
      item_id: 1,
      content: "Milk, Bread, Eggs, Butter",
      completed: false,
    },
    {
      item_id: 2,
      content: "30 minutes of cardio",
      completed: false,
    },
    {
      item_id: 3,
      content: "Read 'Atomic Habits'",
      completed: false,
    },
    {
      item_id: 4,
      content: "Vacuum and dust living room",
      completed: false,
    },
    {
      item_id: 5,
      content: "Complete the frontend for the new app",
      completed: false,
    },
    {
      item_id: 6,
      content: "Check in with mom and see how she's doing",
      completed: false,
    },
    {
      item_id: 7,
      content: "Research destinations and book flights",
      completed: false,
    },
    {
      item_id: 8,
      content: "Buy ingredients for dinner",
      completed: false,
    },
    {
      item_id: 9,
      content: "Pay electricity and water bills",
      completed: false,
    },
    {
      item_id: 10,
      content:
        "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Aspernatur adipisci officiis officia nemo quasi corporis perferendis voluptate tempora quo eaque!",
      completed: false,
    },
  ];

  return (
    <div className="w-full h-full flex flex-col items-center justify-start">
      <div className="w-full flex flex-row items-center justify-between p-2">
      <button className="font-bold px-3 py-2 rounded-lg transition-colors duration-200 bg-nightBlue text-sandTan text-xl hover:opacity-75">
          {"<"}
        </button>
        <h1 className="text-2xl font-bold p-5 text-nightBlueShadow">Todos</h1>
        <button className="font-bold px-3 py-2 rounded-lg transition-colors duration-200 bg-nightBlue text-sandTan text-xl hover:opacity-75">
          {">"}
        </button>
      </div>

      <div className="w-full h-full flex flex-col items-center justify-start overflow-y-auto gap-1 p-2">
        {todos.map((todo) => (
          <Todo
            todo={todo}
            key={todo.id}
          />
        ))}
      </div>
    </div>
  );
}
