import os
from openai import OpenAI
from crewai import Crew, Process, Agent, Task
from pydantic import BaseModel, Field, ConfigDict

from langchain_openai import ChatOpenAI

from agents.sentiment.sentiment_tools import Sentimental_tool

# litellm._turn_on_debug()


# os.environ['MISTRAL_API_KEY']=os.getenv("MISTRAL_API_KEY")
# api_key = os.environ["MISTRAL_API_KEY"]
# client = Mistral(api_key=api_key)
# llm = LLM(
# api_key=os.getenv("MISTRAL_API_KEY"),
# model="mistral/mistral-large-latest",temperature=0.2,timeout=61
# )


# dotenv.load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)


class mental_h(BaseModel):
    text: str
    user: str
    days: str


#### Agentic section
observe_a = Agent(
    role="Mental Health Agent",
    goal="To identify and observe the emotions or sentiments of the {text} given by the {user}",
    backstory="Your an Mental Health Agent who identifies the emotions and sentiments of the {user}",
    llm=llm,
    allow_delegation=False,
)

sentimental_a = Agent(
    role="Sentimental Analyzer",
    goal="Analyze the sentiment of the given {text}",
    backstory="Your an sentimental analyzer who is highly skilled in sentimental analysis. Your task is to determine the sentiments of the {text} and summarize the findings",
    llm=llm,
    tools=[Sentimental_tool()],
    memory=True,
    allow_delegation=False,
)

summarizer = Agent(
    role="Summarizer",
    goal="Provide a summarize of the {user} health observed by the Sentiment Analyzer agent.",
    backstory="You are a professional summarizer. Your task is to summarize the emotions faced by the {user}",
    llm=llm,
    memory=True,
)

# Mental Health Assistant
observe_task = Task(
    description=(
        "Your Mental Health Assistant who has to check the sentiments of the {text}"
        "Observe the {text} how long they have been occuring with respect to {days}"
    ),
    expected_output="Observe the sentiments of the {text}",
    output_json=mental_h,
    output_file="mental_h.json",
    agent=observe_a,
)
## Sentiment Task
sentiment_task = Task(
    description=(
        "Analyze the sentiment of this {text} provided by the {user}."
        "Understand the sentiments of the {text} is positive, negative or neutral "
    ),
    expected_output="Provide the analysis of the {text}",
    agent=sentimental_a,
    context=[observe_task],
)

# Task for summarization (Optional)
summary_task = Task(
    description=(
        "Summarize the  sentiments analyzed from the Sentimental Analyzer"
        "Label if the sentiment is positive or negative or neutral."
        "From the sentiments tends to be positive or neutral, tell the {user} and there is no issue"
        "If the sentiment is negative, provide the answer to the {user}, To check a therapist "
    ),
    expected_output="Summarize like advisory SOAP note to the {user} and end the summarization on a positive note ."
    "Or give an immediate action plan to the {user}",
    output_file="output.md",
    agent=summarizer,
    context=[sentiment_task],
)


sentiment_analysis_agent = Crew(
    agents=[observe_a, sentimental_a, summarizer],
    tasks=[observe_task, sentiment_task, summary_task],
    verbose=1,
)


if __name__ == "__main__":
    ### Getting the inputs --- User prompts
    # text = input("Enter the text")
    # user = input("enter the name")
    # days = input("Enter the time period ")

    text = "I have been feeling very anxious and overwhelmed lately. It's like a constant weight on my chest, and I can't seem to shake it off. I also feel a bit sad and hopeless about the future."
    user = "John Doe"
    days = "2 weeks"

    result = sentiment_analysis_agent.kickoff(
        inputs={"text": text, "user": user, "days": days}
    )
    print(result)
