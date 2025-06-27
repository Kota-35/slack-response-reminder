"""Slackのメッセージを定期的に確認して、未返信のメッセージをリマインドする."""

import uvicorn
from fastapi import FastAPI

from src import api

app = FastAPI()


@app.get("/")
async def hello() -> str:
    """Hello World."""
    return "Hello World"


app.include_router(api.router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)  # noqa: S104
