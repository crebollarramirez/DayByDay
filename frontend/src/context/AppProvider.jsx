import React, { createContext, useState, useContext } from "react";

const AppContext = createContext();

export const AppProvider = ({ children }) => {
  const [selectedTask, setSelectedTask] = useState(null);
  const [selectedTodo, setSelectedTodo] = useState(null);

  return (
    <AppContext.Provider value={{ selectedTask, setSelectedTask, selectedTodo, setSelectedTodo }}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useAppContext must be used within AppProvider');
  }
  return context;
};
