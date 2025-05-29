from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitRemoteEndpoint, Action as CopilotAction
from agents.questionnaire.quest_eval import run

from agents import sentiment_analysis_agent

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

##
# Function to run the sentiment analysis agent
async def run_sentiment_analysis_agent(
    emotion_description: str, user_name: str, days: str
):
    print(f"Running sentiment analysis for")

    payload = {
        "text": emotion_description,
        "user": user_name,
        "days": days,
    }

    # return {"response": "you are all good"}
    crew_output = sentiment_analysis_agent.kickoff(inputs=payload)
    return {"result": crew_output.raw}


sentiment_analysis_action = CopilotAction(
    name="sentimentAnalysis",
    description="perform sentiment analysis of user's given description of self emotion in a fixed period of time",
    parameters=[
        {
            "name": "emotion_description",
            "type": "string",
            "description": "user's description of self emotion",
            "required": True,
        },
        {
            "name": "user_name",
            "type": "string",
            "description": "user's name",
            "required": True,
        },
        {
            "name": "days",
            "type": "string",
            "description": "number of days to analyze",
            "required": True,
        },
    ],
    handler=run_sentiment_analysis_agent,
)

async def run_phq_questionnaire_agent(user_name: str,question_index: str = None, answer: str=None,responses: dict = None):
    if responses is None:
        responses = {}

    print(f"Running PHQ-9 questionnaire agent with question index: {question_index}, answer: {answer}, responses: {responses}")
    # Store the answer for the previous question (if not the first question)
    
      # Convert to int if needed
    if isinstance(question_index, str):
        print(f" Converting question_index from str to int: {question_index}")
        question_index = int(question_index)
    if answer is not None and isinstance(answer, str):
        print(f" Converting answer from str to int: {answer}")
        answer = int(answer)

    if answer is not None and int(question_index) > 0:
        responses[f"Q{question_index}"] = answer
        print(f" Stored response for responses", responses)

    

    if question_index < 0:
        return {
            "question": None,
            "question_index": question_index,
            "responses": responses,
            "has_more": False
        }

    # If all questions answered, call the agent
    if question_index >= len(ph9_q):
        # Optionally, store the last answer if not already stored
        if answer is not None and f"Q{question_index}" not in responses:
            responses[f"Q{question_index}"] = answer

        # Remove any None keys/values
        #responses = {k: v for k, v in responses.items() if v is not None}
        print(f"Collected PH-9 responses: {responses}")
        agent_output = run(responses)

        
        
        print(f"Agent output: {agent_output}")
        # All questions answered, return completion
        return {
            "result": agent_output,
            "completed": True,
            "responses": responses
        }

    return {
        "question": ph9_q[question_index],
        "question_index": question_index + 1,
        "has_more": question_index < len(ph9_q) - 1,
        "completed": False,
        "responses": responses
    }

phq_questionnaire_action = CopilotAction(
    name="phqQuestionnaire",
    description="Ask the user PHQ-9 depression screening questions one at a time",
    parameters=[
        {
            "name": "user_name",
            "type": "string",
            "description": "user's name",
            "required": True,
        },
        {
            "name": "question_index",
            "type": "string",
            "description": "index of the PHQ question to ask",
            "required": True,
        },
        {
            "name": "answer",
            "type": "string",
            "description": "user's answer to the current question (0-3)",
            "required": True,
        },
        {
            "name": "responses",
            "type": "object",
            "description": "dictionary of previous responses",
            "required": False,
        }
    ],
    handler=run_phq_questionnaire_agent,
)

# Initialize the CopilotKit SDK
sdk = CopilotKitRemoteEndpoint(actions=[sentiment_analysis_action, phq_questionnaire_action])

# Add the CopilotKit endpoint to your FastAPI app
add_fastapi_endpoint(app, sdk, "/copilotkit_remote")


def main():
    """Run the uvicorn server."""
    import uvicorn

    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
