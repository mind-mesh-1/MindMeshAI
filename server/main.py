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


# Initialize the CopilotKit SDK
sdk = CopilotKitRemoteEndpoint(actions=[sentiment_analysis_action])

# Add the CopilotKit endpoint to your FastAPI app
add_fastapi_endpoint(app, sdk, "/copilotkit_remote")


def main():
    """Run the uvicorn server."""
    import uvicorn

    uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    main()
