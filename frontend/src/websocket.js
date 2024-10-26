import { ACCESS_TOKEN } from "./constants";

const createWebSocket = () => {
    // Define the WebSocket endpoint; it might look like ws://127.0.0.1:8000/ws/some_endpoint
    const socketUrl = `ws://127.0.0.1:8000/ws/chat/`;
  
    const token = localStorage.getItem(ACCESS_TOKEN);
    const socket = new WebSocket(`${socketUrl}?token=${token}`); // Append token if needed
  
    socket.onopen = () => {
      console.log("WebSocket connection opened");
      // You can send a message if needed immediately after opening
    };
  
    socket.onmessage = (event) => {
      const data = JSON.parse(event.data);
      console.log("Received message from WebSocket:", data);
      // Handle incoming messages here
    };
  
    socket.onclose = (event) => {
      if (event.wasClean) {
        console.log("WebSocket closed cleanly");
      } else {
        console.error("WebSocket connection closed unexpectedly");
      }
    };
  
    socket.onerror = (error) => {
      console.error("WebSocket error:", error);
    };
  
    return socket;
  };
  
  export default createWebSocket;