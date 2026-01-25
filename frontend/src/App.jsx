import { Header } from "./components/header.jsx";
import { Agent } from "./components/agent.jsx";
import "./App.css";

export default function App() {

  return (
    <div
      style={{
        width: "100%",
        margin: "0 auto",
        height: "100%",
        padding: "20px",
        fontFamily: "Inter, system-ui, Arial",
        background: "#33b49d",
      }}
    >
      <Header />
      <Agent />
    </div>
  );
}
