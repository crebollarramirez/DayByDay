import React, { useEffect, useState } from "react";
import { TodosBox } from "./components/TodosBox";
import api from "./api";
import { CreateTodoBlock } from "./components/CreateTodoBlock";
import { Week } from "./components/Week/Week";

function App() {
  const [todos, setTodos] = useState([]);
  const [week, setWeek] = useState([[]])

  useEffect(() => {
    getTodos();
    getWeek();
  }, []);

  const getTodos = () => {
    api
      .get("./api/todos/list/")
      .then((res) => res.data)
      .then((data) => {
        setTodos(data);
        console.log(data)
      })
      .catch((err) => alert(err));
  };

  const getWeek = () => {
    api
    .get("./api/week/list/")
    .then((res) => res.data)
    .then((data) => {
      setWeek(data);
      console.log("This is the week")
      console.log(data)
    })
    .catch((err) => alert(err))
  };

  return (
    <main>
      <TodosBox getTodos={getTodos} todos={todos} />
      <CreateTodoBlock getTodos={getTodos} />
      <Week />
    </main>
  );
}

export default App;
