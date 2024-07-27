import React, { useEffect, useState } from 'react';
import axios from 'axios';
import {Week} from "./Week"
import {Today} from "./Today"
import {Info} from "./Info"
import "./style.css"

function App() {
  const [data, setData] = useState(null);

  useEffect(() => {
    axios.get('http://127.0.0.1:5000/api/data')
      .then(response => {
        setData(response.data);
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  }, []);

  return (
    <>
      <main>      
        <div className="grid-container">
        <Week className="week grid-item"/>
        <Today className="today grid-item"/>
        <Info className="info grid-item"/>
      </div>
      </main>


      {/* <h1>Data from Flask (backend):</h1>
      {data && <pre>{JSON.stringify(data, null, 2)}</pre>} */}
    </>
  );
}

export default App;