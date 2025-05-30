from langchain_core.prompts import ChatPromptTemplate
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import tool
import dotenv
import os
from langchain_openai import ChatOpenAI
from openai import OpenAI
import json
from typing import Dict


@tool("PHQ9ScorerTool", return_direct=False)
def evaluation_score(responses:str)->str:
    """Interprets PH9-Q Questionnaire and evaluates the score, the severity and suicidal thought """
    print("Inside evaluation_score responses:", responses)
    phq9_data: Dict[str, int] = json.loads(responses)
    cleaned_responses = {}
    for k, v in phq9_data.items():
        try:
            cleaned_responses[k] = int(v)
        except (ValueError, TypeError):
            print(f"Warning: Non-integer value encountered for {k}. Using 0.")
            cleaned_responses[k] = 0

    score=sum(cleaned_responses.values())
    suicidal_score = cleaned_responses.get("Q9", 0) > 0

    def interpret_score(score):
        if 0 <= score <= 4: 
            return "Minimal"
        elif 5 <= score <= 9: 
            return "Mild"
        elif 10 <= score <= 14: 
            return "Moderate"
        elif 15 <= score <= 19: 
            return "Moderately Severe"
        elif 20 <= score <= 27: 
            return "Severe"
        else:
            return "Invalid"

    total_score=interpret_score(score)

    results={
        "score":score,
        "total_score":total_score,
        "suicidal_score":suicidal_score
    }
    result_json=json.dumps(results)
    return result_json


dotenv.load_dotenv()
os.environ['OPENAI_API_KEY']=os.getenv("OPENAI_API_KEY")

def run(responses):

    print("Inside run responses:", responses)
    llm = ChatOpenAI(
    model="gpt-4o-mini", temperature =0.2
    )
    
    prompt=hub.pull("hwchase17/react")
    tools=[evaluation_score]
    agent = create_react_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True
    )
    pre_collected_responses = json.dumps(responses)
    print("TEST before agentexecutor")
    agent_output = agent_executor.invoke(
        {
            "input": f"Please interpret the following PHQ-9 responses: {pre_collected_responses}."
                     "You're Mental Health Assistant to check if the patient is suffering from depression"
                     "Provide a compassionate note summary of the mental health assessment, "
                     "including the total score, depression severity, and suicidal ideation indication. "
                     "If the suicidal ideation is higher and let the patient know immediately"
                     "Conclude with a clear recommendation for professional help, If its severe, raise an alarm for emergency in case of sucidal thought. End it with a positive note"
       }
    )
    print("Agent output:", agent_output['output'])
    return agent_output['output']
