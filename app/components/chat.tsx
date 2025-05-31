import { CopilotKit } from "@copilotkit/react-core";
import { CopilotChat } from "@copilotkit/react-ui";
import { useEffect, useState } from "react";
 
export function ChatAgent() {


  return (
    <div>
      <CopilotKit runtimeUrl="api/copilotkit">
        <div style={{ height: "80vh", maxHeight: "80vh", overflow: "auto" }}>
            <CopilotChat
            instructions={
               "First, ask the user to describe their current mood. " +
               "After analyzing, guide them through the PHQ-9 questionnaire, asking one question at a time and collecting their answers. " +
               "After all questions are answered, summarize the results compassionately."
            }
            labels={{
                title: "Your Assistant",
                initial: "Hi! 👋 I am Mindmesh AI an assistant for your mental health? How are you feeling today?",
                placeholder: "type your message here...",
              }}
            />
        </div>
    </CopilotKit>
    </div>     
  );
}