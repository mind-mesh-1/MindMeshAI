from langchain_core.prompts import ChatPromptTemplate
from langchain import hub
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import tool
import dotenv
import os
from langchain_openai import ChatOpenAI
from openai import OpenAI
import json

ph9_q=["Over the last two weeks, how often have you been bothered by little interest or pleasure in doing things? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by feeling down, depressed, or hopeless? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by trouble falling or staying asleep, or sleeping too much? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by feeling tired or having little energy? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by poor appetite or overeating? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by feeling bad about yourself – or that you are a failure or have let yourself or your family down? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by trouble concentrating on things, such as reading the newspaper or watching television? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by moving or speaking so slowly that other people could have noticed? Or the opposite – being so restless that you have to move around a lot more than usual? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by thoughts that you would be better off dead or of hurting yourself in some way? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): "
]
responses={}
for i, q in enumerate(ph9_q):
    while True:
        try:
            user_response=input(f"Q{i+1}:{q}")
            user_response_int=int(user_response)
            if 0<=user_response_int <=3:
                responses[f"Q{i+1}"]=user_response_int
                break
            else:
                print("Please enter a number between 0 and 3")
        except ValueError:
            print("Invalid number")

### React agent
@tool("PHQ9ScorerTool", return_direct=False)
def interpret_score(responses:str)->str:
    """Interprets PH9-Q Questionnaire and evaluates the score, the severity and suicidal thought """
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


client = OpenAI(
    api_key = os.environ.get("OPENAI_API_KEY")
)
llm = ChatOpenAI(
    model="gpt-4o-mini", temperature =0.5
)
prompt=hub.pull("hwchase17/react")
tools=[interpret_score]
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,
    handle_parsing_errors=True
)
pre_collected_responses = json.dumps(responses)
agent_output = agent_executor.invoke(
    {
        "input": f"Please interpret the following PHQ-9 responses: {pre_collected_responses}. "
                 "Provide a compassionate SOAP note summary of the mental health assessment, "
                 "including the total score, depression severity, and suicidal ideation indication. "
                 "Conclude with a clear recommendation for professional help, If its severe, raise an alarm for emergency in case of sucidal thought. End it with a positive note"
    }
)

