
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "fastapi",
#     "uvicorn",
#     "vaderSentiment",
# ]
# ///

from fastapi import FastAPI
from pydantic import BaseModel
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import os

app = FastAPI()

analyzer = SentimentIntensityAnalyzer()


class SentimentRequest(BaseModel):
    sentences: list[str]


@app.get("/")
async def home():
    return {"message": "Sentiment API is running"}


@app.post("/sentiment")
async def analyze_sentiment(request: SentimentRequest):
    results = []

    for sentence in request.sentences:
        score = analyzer.polarity_scores(sentence)["compound"]

        if score >= 0.05:
            sentiment = "happy"
        elif score <= -0.05:
            sentiment = "sad"
        else:
            sentiment = "neutral"

        results.append({
            "sentence": sentence,
            "sentiment": sentiment
        })

    return {"results": results}


if __name__ == "__main__":
    import uvicorn

    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
