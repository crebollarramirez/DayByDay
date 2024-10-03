import React, { useEffect, useState } from "react";
import { TodosBox } from "./components/TodosBox";
import api from "./api";
import { CreateTodoBlock } from "./components/CreateTodoBlock";
import { Week } from "./components/Week/Week";
import { Today } from "./components/Today";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom"
import ProtectedRoute from "./components/ProtectedRoute";
import Home from "./pages/Home";
import Login from "./pages/Login";
import NotFound from "./pages/NotFound";
import Register from "./pages/Register";
// const [todos, setTodos] = useState([]);

// useEffect(() => {
//   getTodos();
// }, []);

// const getTodos = () => {
//   api
//     .get("./api/todos/list/")
//     .then((res) => res.data)
//     .then((data) => {
//       setTodos(data);
//     })
//     .catch((err) => alert(err));
// };

function Logout() {
  localStorage.clear();
  return <Navigate to="/login" />;
}

function RegisterAndLogout() {
  localStorage.clear();
  return <Register />;
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/"
          element={
            <ProtectedRoute>
              <Home />
            </ProtectedRoute>
          }
        />
        <Route path="/login" element={<Login />} />
        <Route path="/logout" element={<Logout />} />
        <Route path="/register" element={<RegisterAndLogout />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
