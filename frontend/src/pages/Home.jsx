import { CreateMenu } from "../components/BottomViews/CreateMenu";
import Form from "../components/Form";
import { TodosBox } from "../components/BottomViews/TodosBox";
import React, { useState, useEffect } from "react";
import api from "../api";
import { Week } from "../components/Week/Week";
import { Today } from "../components/BottomViews/Today";
import "./../styles/homeStyle.css";
import { QuoteOfTheDay } from "../components/BottomViews/QuoteOfTheDay";
import { Chat } from "../components/AIChat/Chat";

function Home() {
  const [todos, setTodos] = useState([]);
  const [isCreateMenuVisible, setIsCreateMenuVisible] = useState(false); // State for CreateMenu visibility

  useEffect(() => {
    getTodos();
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

  const toggleCreateMenu = () => {
    setIsCreateMenuVisible(!isCreateMenuVisible); // Toggle visibility
  };

  return (
    <div className="main-container">
      <main>
        <Week />
        <div className="bottomItems-container">
          <div className="bottomView">
            <Today toggleCreateMenu={toggleCreateMenu} />
            <TodosBox getTodos={getTodos} todos={todos} />
            {isCreateMenuVisible ? (
              <CreateMenu getTodos={getTodos} />
            ) : (
              <QuoteOfTheDay />
            )}
            <Chat />
          </div>
        </div>
      </main>
    </div>
  );
}

export default Home;
