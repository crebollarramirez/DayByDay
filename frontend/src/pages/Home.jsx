import { CreateTodoBlock } from "../components/CreateTodoBlock";
import Form from "../components/Form";
import { TodosBox } from "../components/TodosBox";
import React, {useState, useEffect} from "react"
import api from "../api";

function Home() {
  const [todos, setTodos] = useState([]);
  useEffect(() => {
  getTodos();
  }, [])

  const getTodos = () => {
    api
      .get("./api/todos/")
      .then((res) => res.data)
      .then((data) => {
        setTodos(data);
      })
      .catch((err) => alert(err));
  };

  return (
    <main>
      <h1>this is the home page</h1>
      <TodosBox getTodos={getTodos} todos={todos}/>
      <CreateTodoBlock getTodos={getTodos}/>
    </main>
  );
}

export default Home;
