import { useState } from "react";
import { useNavigate } from "react-router-dom";
import useAuth from "../auth/useAuth";
import "./Login.css"

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const { login } = useAuth();
  const [showPassword, setShowPassword] = useState(false);
  const handleLogin = () => {
    login(username);

    if (username === "admin" && password==="admin") {
      navigate("/admin");
    } 
    else if (username==="customer" && password==="customer") {
      navigate("/chat");
    }
    else {
      alert ("You have entered incorrect USER ID or Password ")
    }
  };

  return (
    <div className="card">
      <h2><b>Welcome to ABC Bank</b> </h2>
      

      <input
        placeholder="Username (admin / customer)"
        onChange={(e) => setUsername(e.target.value)}
      /><br></br>
      <div className="password-wrapper">
      <input
        type={showPassword ? "text" : "password"}
        placeholder="Password"
        onChange={(e) => setPassword(e.target.value)}
      />

      <span
        className="toggle-eye"
        onClick={() => setShowPassword(!showPassword)}
      >
        {showPassword ? "🙈" : "👁️"}
      </span>
    </div>

      <br/><br/>
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}
