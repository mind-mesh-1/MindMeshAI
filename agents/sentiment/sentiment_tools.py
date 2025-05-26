from crewai.tools import BaseTool
from textblob import TextBlob
from typing import List, Dict, Any
from pydantic import BaseModel, Field, ConfigDict


class Sentimental_tool(BaseTool):
    """
    Analyze the sentiment of the text using Text Blob
    """

    name: str = "Sentiment Analysis Tool"
    description: str = (
        "Analyzes the sentiment of the given text and returns polarity and subjectivity scores."
    )
    text: str = Field(default="", description="The text to analyze")

    def _run(self, text: str = "") -> Dict[str, float]:
        """
        Analyze the sentiment of the text using Text Blob

        Args:
        text (str): The text to analyze.

        Returns:
            Dict[str, float]: A dictionary containing the polarity and subjectivity scores.
            - polarity: Ranges from -1 (most negative) to 1 (most positive).
            - subjectivity: Ranges from 0 (objective) to 1 (subjective).
        """
        if not text:
            return {"polarity": 0.0, "subjectivity": 0.0}

        analysis = TextBlob(text)
        return {
            "polarity": analysis.sentiment.polarity,
            "subjectivity": analysis.sentiment.subjectivity,
        }
