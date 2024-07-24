// client/src/components/TodoList.js
import React, { useEffect, useState } from 'react';
import api from '../api';

const TodoList = () => {
  const [todos, setTodos] = useState([]);

  useEffect(() => {
    const fetchTodos = async () => {
      const response = await api.get('/api/todos');
      setTodos(response.data);
    };

    fetchTodos();
  }, []);

  return (
    <div>
      {todos.map(todo => (
        <div key={todo.id}>{todo.title}</div>
      ))}
    </div>
  );
};

export default TodoList;