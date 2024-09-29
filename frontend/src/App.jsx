import React, { useEffect, useState } from "react";
import { TodosBox } from "./components/TodosBox";
import api from "./api";
import { CreateTodoBlock } from "./components/CreateTodoBlock";
import { Week } from "./components/Week/Week";
import { Today } from "./components/Today";

function App() {
  const [todos, setTodos] = useState([]);

  useEffect(() => {
    getTodos();
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


  return (
    <main>
      <TodosBox getTodos={getTodos} todos={todos} />
      <CreateTodoBlock getTodos={getTodos} />
      <Week/>
      <Today />
    </main>
  );
}

export default App;
