import React, { useState, useEffect } from "react";
import api from "../api";

const QuoteOfTheDay = () => {
  const [quote, setQuote] = useState(
    "Today is the day we have been waiting for."
  );
  const [author, setAuthor] = useState("Tony Robbins");

  const fetchQuote = async () => {
    try {
      const response = await api.get("/quote");
      setQuote(response.data.quote);
      setAuthor(response.data.author);
    } catch (error) {}
  };

  return (
    <div className="w-full h-full flex flex-col items-center justify-center">
      <h1 className="p-4">Quote of the Day</h1>
      <div className="w-[40%] h-full flex flex-col items-center justify-center">
        <p className="text-xl italic font-semibold text-gray-800 w-full">
          {quote}
        </p>
        <div className="flex flex-row w-full justify-end">
          <p className="text-right text-gray-600">- {author}</p>
        </div>
      </div>
    </div>
  );
};

export default QuoteOfTheDay;
