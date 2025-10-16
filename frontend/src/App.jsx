import React, { useState } from "react";
import ChatBox from "./ChatBox";

function App() {
  const [messages, setMessages] = useState([]);

  const sendMessage = async (msg) => {
    if (!msg.trim()) return;

    const userMessage = { sender: "user", text: msg };
    setMessages((prev) => [...prev, userMessage]);

    const res = await fetch("http://localhost:7860/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: msg }),
    });

    const data = await res.json();
    const botMessage = { sender: "bot", text: data.reply };
    setMessages((prev) => [...prev, botMessage]);
  };

  return (
    <div>
      <h2>🧠 Generative AI Chat Assistant</h2>
      <ChatBox messages={messages} onSend={sendMessage} />
    </div>
  );
}

export default App;
