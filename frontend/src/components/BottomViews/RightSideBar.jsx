import React, { useState } from "react";
import "../../styles/rightSideBarStyle.css";
import { Chat } from "../../components/AIChat/Chat";
import api from "../../api";
import { CreateMenu } from "./CreateMenu";

export function RightSideBar({ getTodos }) {
  return (
    <div className="rightBar-container">
      <CreateMenu getTodos={getTodos} />
      <Chat />
    </div>
  )
}
