from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitRemoteEndpoint, Action as CopilotAction

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


##
# Function to run the sentiment analysis agent
async def run_sentiment_analysis_agent(
    emotion_description: str, user_name: str, days: str
):

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

async def run_phq_questionnaire_agent(user_name: str, question_index: int = 0):
    # You can customize the questions as needed
    phq_questions = [
        "Over the last two weeks, how often have you been bothered by little interest or pleasure in doing things? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by feeling down, depressed, or hopeless? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by trouble falling or staying asleep, or sleeping too much? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by feeling tired or having little energy? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by poor appetite or overeating? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by feeling bad about yourself – or that you are a failure or have let yourself or your family down? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by trouble concentrating on things, such as reading the newspaper or watching television? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by moving or speaking so slowly that other people could have noticed? Or the opposite – being so restless that you have to move around a lot more than usual? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): ",
        "Over the last two weeks, how often have you been bothered by thoughts that you would be better off dead or of hurting yourself in some way? (0 = Not at all, 1 = Several days, 2 = More than half the days, 3 = Nearly every day): "
    ]

    if question_index < 0 or question_index > len(phq_questions):
        return {
            "user": user_name,
            "question": None,
            "question_index": question_index,
            "has_more": False
        }
    return {
        "user": user_name,
        "question": phq_questions[question_index],
        "question_index": question_index,
        "has_more": question_index < len(phq_questions) - 1
    }

phq_questionnaire_action = CopilotAction(
    name="phqQuestionnaire",
    description="ask the user PHQ-9 depression screening questions",
    parameters=[
        {
            "name": "user_name",
            "type": "string",
            "description": "user's name",
            "required": True,
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
