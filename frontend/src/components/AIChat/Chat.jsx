import React, { useState, useEffect, useRef } from "react";
import "../../styles/chatStyle.css";
import api from "../../api";

export function Chat() {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const chatWindowRef = useRef(null); // Create a ref for the chat window

  const sendMessage = async () => {
    if (!newMessage.trim()) return; // Prevent empty messages
    // Update local chat with user message
    const userMessage = { text: newMessage, sender: "user" };
    setMessages([...messages, userMessage]);

    // Send message to backend
    try {
      const response = await api.post("api/chat/", { message: newMessage });
      const botMessage = { text: response.data.reply, sender: "bot" };
      setMessages([...messages, userMessage, botMessage]); // Add bot response
    } catch (error) {
      console.error("Error sending message", error);
    }
    setNewMessage("");
  };

  // Scroll to the bottom of the chat window whenever messages change
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]); // Run this effect whenever messages change

  return (
    <div className="chat-container">
      <h1>AI CHAT</h1>
      <div className="chat-window" ref={chatWindowRef}>
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.text}
          </div>
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type your message..."
        />
        <button className="sendButton" onClick={sendMessage}>
          Send
        </button>
      </div>
    </div>
  );
}
