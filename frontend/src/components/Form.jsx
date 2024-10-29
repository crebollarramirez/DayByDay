import { useState } from "react";
import api from "../api";
import { useNavigate } from "react-router-dom";
import { ACCESS_TOKEN, REFRESH_TOKEN } from "../constants";
import "../styles/formStyle.css";
import LoadingIndictor from "./LoadingIndicator";

function Form({ route, method }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const name = method === "login" ? "Login" : "Register";

  const handleSubmit = async (e) => {
    setLoading(true);
    e.preventDefault();

    try {
      const res = await api.post(route, { username, password });
      if (method === "login") {
        localStorage.setItem(ACCESS_TOKEN, res.data.access);
        localStorage.setItem(REFRESH_TOKEN, res.data.refresh);
        navigate("/");
      } else {
        navigate("/login");
      }
    } catch (error) {
      alert(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="form-container">
      <h1>{name}</h1>
      <div className="fields-container">
        <div className="form__group field">
          <input
            className="form__field"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username"
          />
          <label htmlFor="content" className="form__label">
            Username
          </label>
        </div>
        <div className="form__group field">
          <input
            className="form__field"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password"
          />
          <label htmlFor="content" className="form__label">
            Password
          </label>
        </div>
      </div>

      {loading && <LoadingIndictor />}
      <button className="submit-button" type="submit">
        {name}
      </button>
    </form>
  );
}

export default Form;
