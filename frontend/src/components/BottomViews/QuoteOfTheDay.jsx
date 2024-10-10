import React from "react";
import "../../styles/quoteOfTheDayStyle.css";

export function QuoteOfTheDay() {
  return (
    <div className="quote-box">
      <h1>Quote of the Day</h1>
      <div className="quote-container">
        <q className="quote">
          Believe you can, and you're halfway there.
        </q>

        <div className="author">– Theodore Roosevelt</div>
      </div>
    </div>
  );
}
