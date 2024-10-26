import React, { useState, useEffect, useRef } from "react";
import "../../styles/chatStyle.css";
import createWebSocket from "../../websocket"; // Assume websocket.js has the WebSocket creation logic

export function Chat() {
  const [messages, setMessages] = useState([]);
  const [newMessage, setNewMessage] = useState("");
  const chatWindowRef = useRef(null);
  const socketRef = useRef(null);

  // Initialize WebSocket connection
  useEffect(() => {
    // Create the WebSocket connection and store it in a ref
    socketRef.current = createWebSocket();

    // Handle incoming messages from WebSocket
    socketRef.current.onmessage = (event) => {
      const data = JSON.parse(event.data);
      const botMessage = { text: data.reply, sender: "bot" };
      setMessages((prevMessages) => [...prevMessages, botMessage]);
    };

    // Clean up WebSocket on component unmount
    return () => {
      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, []);

  // Send message to WebSocket
  const sendMessage = () => {
    if (!newMessage.trim()) return; // Prevent empty messages

    const userMessage = { text: newMessage, sender: "user" };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    // Send message through WebSocket
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      socketRef.current.send(JSON.stringify({ message: newMessage }));
    } else {
      console.error("WebSocket is not open.");
    }

    setNewMessage("");
  };

  // Scroll to the bottom of the chat window whenever messages change
  useEffect(() => {
    if (chatWindowRef.current) {
      chatWindowRef.current.scrollTop = chatWindowRef.current.scrollHeight;
    }
  }, [messages]);

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
