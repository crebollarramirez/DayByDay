import React, { useEffect, useState } from "react";
import api from "../api";
import { Todo } from "./Todo";

export function TodosBox() {
  // Function to delete a task
  // const deleteTodo = async (item_id, item_type) => {
  //   try {
  //     const response = await api.delete(
  //       `api/todos/delete/${item_id}/${item_type}`
  //     );

  //     if (response.status === 204) {
  //       console.log("Task deleted successfully");
  //       // Optionally refresh tasks or update state here
  //     } else {
  //       console.error("Failed to delete the task");
  //     }
  //   } catch (error) {
  //     console.error("Failed to delete the task", error);
  //   }
  //   getTodos();
  // };

  // const editTodo = async (item_id, item_type, newData = {
  //   content: "testing",
  // }) => {
  //   try {
  //     const response = await api.put(`api/todos/edit/${item_id}/${item_type}`, newData);

  //     if (response.status === 204) {
  //       console.log("Todo was edited successfully");
  //     } else {
  //       console.error("failed to edit the todo");
  //     }
  //   } catch (error) {
  //     console.error("Failed to edit the todo", error);
  //   }
  //   getTodos();
  // };
  const todos = [
    {
      id: 1,
      title: "Buy groceries",
      content: "Milk, Bread, Eggs, Butter",
      completed: false,
    },
    {
      id: 2,
      title: "Workout",
      content: "30 minutes of cardio",
      completed: false,
    },
    {
      id: 3,
      title: "Read a book",
      content: "Read 'Atomic Habits'",
      completed: false,
    },
    {
      id: 4,
      title: "Clean the house",
      content: "Vacuum and dust living room",
      completed: false,
    },
    {
      id: 5,
      title: "Finish project",
      content: "Complete the frontend for the new app",
      completed: false,
    },
    {
      id: 6,
      title: "Call mom",
      content: "Check in with mom and see how she's doing",
      completed: false,
    },
    {
      id: 7,
      title: "Plan vacation",
      content: "Research destinations and book flights",
      completed: false,
    },
    {
      id: 8,
      title: "Grocery shopping",
      content: "Buy ingredients for dinner",
      completed: false,
    },
    {
      id: 9,
      title: "Pay bills",
      content: "Pay electricity and water bills",
      completed: false,
    },
    {
      id: 10,
      title: "Go for a walk",
      content:
        "Lorem ipsum dolor sit, amet consectetur adipisicing elit. Aspernatur adipisci officiis officia nemo quasi corporis perferendis voluptate tempora quo eaque!",
      completed: false,
    },
  ];

  return (
    <div className="w-full h-full flex flex-col items-center justify-start">
      <h1 className="text-2xl font-bold p-5 text-nightBlueShadow">Todos</h1>

      <div className="w-full h-full flex flex-col items-center justify-start overflow-y-auto gap-1 p-2">
        {todos.map((todo) => (
          <Todo
            todo={todo}
            // onDelete={deleteTodo}
            // onEdit={editTodo}
            key={todo.id}
            // getTodos={getTodos}
          />
        ))}
      </div>
    </div>
  );
}
