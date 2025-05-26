import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import { useEffect, useState } from "react";
 
export function ChatAgent() {

  const [greeting, setGreeting] = useState("");

  useEffect(() => {
    fetch("http://localhost:8000/api/greet?name=NextUser")
      .then((res) => res.json())
      .then((data) => setGreeting(data.message))
      .catch((err) => console.error("API error:", err));
  }, []);

  return (
    <div>
      <p className="text-lg mb-4">{greeting}</p>
      <CopilotKit runtimeUrl="api/copilotkit">
            <CopilotChat
              instructions={"You are assisting the user as best as you can. Answer in the best way possible given the data you have."}
              labels={{
                title: "Your Assistant",
                initial: "Hi! 👋 I am Mindmesh AI an assistant for your mental health? How are you feeling today?",
                placeholder: "type your message here...",
              }}
            />
    </CopilotKit>
    </div>     
  );
}