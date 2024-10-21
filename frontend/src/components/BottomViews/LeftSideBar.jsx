import React from "react";
import api from "../../api";
import '../../styles/leftBarStyle.css'
import { TodosBox } from "./TodosBox";

export function LeftSideBar({getTodos, todos}){
    return (
        <div className="leftBar-container">
            <TodosBox getTodos={getTodos} todos={todos}/>
        </div>
    )
}
