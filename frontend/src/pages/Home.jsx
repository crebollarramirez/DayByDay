import { RightSideBar } from "../components/BottomViews/RightSideBar";
import { LeftSideBar } from "../components/BottomViews/LeftSideBar";
import Form from "../components/Form";
import { TodosBox } from "../components/BottomViews/TodosBox";
import React, { useState, useEffect } from "react";
import api from "../api";
import { Week } from "../components/Week/Week";
import { Today } from "../components/BottomViews/Today";
import "./../styles/homeStyle.css";
import { QuoteOfTheDay } from "../components/BottomViews/QuoteOfTheDay";


function Home({user="User"}) {
  const [todos, setTodos] = useState([]);
  const [isCreateMenuVisible, setIsCreateMenuVisible] = useState(false); // State for CreateMenu visibility
  const [username, setUsername] = useState("User")

  useEffect(() => {
    getTodos();
    getUserName();
  }, []);

  const getTodos = () => {
    api 
      .get("./api/todos/")
      .then((res) => res.data)
      .then((data) => {
        setTodos(data);
        console.log(data)
      })
      .catch((err) => alert(err));
  };

  const getUserName = () => {
    api 
      .get("./api/username/")
      .then((res) => res.data)
      .then((data) => {
        setUsername(data)
        console.log(data)
      })
      .catch((err) => alert(err));
  };

  const toggleCreateMenu = () => {
    setIsCreateMenuVisible(!isCreateMenuVisible); // Toggle visibility
  };

  return (
    <div className="main-container">
      <h1>Welcome {username}</h1>
      <main>
        <LeftSideBar getTodos={getTodos} todos={todos}/>
        <Week />
        <RightSideBar getTodos={getTodos} />
      </main>
    </div>
  );
}

export default Home;
