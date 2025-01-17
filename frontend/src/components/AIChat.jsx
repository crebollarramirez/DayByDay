import React, { useState, useEffect, useRef } from "react";
import createWebSocket from "../websocket"; // Assume websocket.js has the WebSocket creation logic

export function AIChat() {
  const [messages, setMessages] = useState([
    { sender: 'user', text: 'Hello, how are you?' },
    { sender: 'ai', text: 'I am good, thank you! How can I assist you today?' },
    { sender: 'user', text: 'Can you tell me a joke?' },
    { sender: 'ai', text: 'Sure! Why don’t scientists trust atoms? Because they make up everything!' },
  ]);
  const [newMessage, setNewMessage] = useState("");
  const chatWindowRef = useRef(null);
  const socketRef = useRef(null);

  // Initialize WebSocket connection
  useEffect(() => {
    // // Create the WebSocket connection and store it in a ref
    // socketRef.current = createWebSocket();

    // // Handle incoming messages from WebSocket
    // socketRef.current.onmessage = (event) => {
    //   const data = JSON.parse(event.data);
    //   console.log("Received message from WebSocket:", data); // Debugging: log received message

    //   // Check the structure of the incoming data
    //   if (data.message) {
    //     const botMessage = { text: data.message, sender: "bot" };
    //     setMessages((prevMessages) => [...prevMessages, botMessage]);
    //   } else {
    //     console.error(
    //       "Received message does not contain 'message' property:",
    //       data
    //     ); // Debugging: log error
    //   }
    // };

    // socketRef.current.onopen = () => {
    //   console.log("WebSocket connection established"); // Debugging: log when connection is opened
    // };

    // socketRef.current.onerror = (error) => {
    //   console.error("WebSocket error observed:", error); // Debugging: log WebSocket errors
    // };

    // socketRef.current.onclose = (event) => {
    //   console.log("WebSocket connection closed:", event); // Debugging: log when connection is closed
    // };

    // // Clean up WebSocket on component unmount
    // return () => {
    //   if (socketRef.current) {
    //     console.log("Closing WebSocket connection"); // Debugging: log when closing connection
    //     socketRef.current.close();
    //   }
    // };


  }, []);

  // Send message to WebSocket
  const sendMessage = () => {
    if (!newMessage.trim()) return; // Prevent empty messages

    const userMessage = { text: newMessage, sender: "user" };
    setMessages((prevMessages) => [...prevMessages, userMessage]);

    // Send message through WebSocket
    if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
      console.log("Sending message to WebSocket:", userMessage); // Debugging: log the message being sent
      socketRef.current.send(JSON.stringify({ message: newMessage }));
    } else {
      console.error(
        "WebSocket is not open. Current state:",
        socketRef.current.readyState
      ); // Debugging: log the state of the WebSocket
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
    <div className="w-full h-full bg-nightBlueShadow rounded-lg shadow-lg">
      <h1 className="text-2xl font-bold p-4 text-dustyWhite text-center">
        AI CHAT
      </h1>

      {/* Chat Container */}
      {/* Chat Container */}
      <div
        ref={chatWindowRef}
        className="chat-window h-[calc(100%-120px)] overflow-y-auto p-4 bg-nightBlue rounded-lg mb-4"
      >
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`mb-4 ${
              msg.sender === "user"
                ? "flex justify-end"
                : "flex justify-start"
            }`}
          >
            <p className={`p-2 rounded-md text-nightBlueShadow ${msg.sender === "user" ? "bg-sandTan" : "bg-sanTanShadow"}`}>{msg.text}</p>
          </div>
        ))}
      </div>

      {/* Input Container */}
      <div className="input-container flex gap-2">
        <input
          type="text"
          value={newMessage}
          onChange={(e) => setNewMessage(e.target.value)}
          placeholder="Type your message..."
          className="flex-1 p-2 rounded-lg bg-nightBlue text-dustyWhite placeholder-dustyWhite/50 border border-sandTan focus:outline-none focus:border-sanTanShadow"
          onKeyPress={(e) => e.key === "Enter" && sendMessage()}
        />
        <button
          className="px-6 py-2 bg-sandTan hover:bg-sanTanShadow text-nightBlueShadow font-bold  rounded-lg transition-colors duration-200"
          onClick={sendMessage}
        >
          Send
        </button>
      </div>
    </div>
  );
}
