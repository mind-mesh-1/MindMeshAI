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
            instructions={
               "First, ask the user to describe their current mood. " +
               "After analyzing their sentiment, guide them through the PHQ-9 questionnaire, asking one question at a time and collecting their answers. " +
               "After all questions are answered, summarize the results compassionately."
            }
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