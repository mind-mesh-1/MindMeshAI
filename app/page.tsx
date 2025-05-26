"use client"
import { CopilotKit } from "@copilotkit/react-core";

import { CopilotSidebar } from "@copilotkit/react-ui";
import "@copilotkit/react-ui/styles.css";
import { ChatAgent } from "./components/chat"; 

export default function Home() {

  
  return (
    
    <div className="min-h-screen bg-gray-100">
      <header className="flex justify-between items-center">
        <h1 className="text-4xl sm:text-5xl font-bold tracking-[-.01em] text-center sm:text-left font-[family-name:var(--font-geist-mono)]">MindMesh </h1>
        
      </header>
      <main className="grid grid-cols-1 lg:grid-cols-2 gap-6"> 
        <div className="text-sm/6 text-center sm:text-center font-[family-name:var(--font-geist-mono)]">
          Your AI-Powered Mind Therapy Assistant
          <br />
          <br />
          <p className="text-lg text-gray-500">
            MindMesh is a mental health assistant that uses AI to provide personalized support and resources for your mental well-being.
            Whether you're looking for coping strategies, mindfulness exercises, or just someone to talk to, MindMesh is here to help.
            <br />
            <br />
            
          </p>
          <img 
        src="/brain.png" 
        alt="MindMesh Logo"
        width={300}
        height={200}
        className="w-full max-w-3xl rounded-lg mx-auto"
      />
        </div>
        <div>
          <ChatAgent />
        </div>
        <div className="flex flex-col items-center justify-left">
          </div>

       
     
        <div className="flex gap-4 items-center flex-col sm:flex-row">
          
        </div>
      </main>
      <footer className="row-start-3 flex gap-[24px] flex-wrap items-center justify-center">
      </footer>
    </div>
  );
}
