"""
api.py - the FastAPI back end.
Run with:  uvicorn api:app --reload
Then open http://127.0.0.1:8000/docs to test every endpoint.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import tools
from agent import handle_request

app = FastAPI(title="FixIt Booking Agent")


class RequestBody(BaseModel):
    message: str


@app.post("/request")
def post_request(body: RequestBody):
    """Run the agent on the customer's message and return the final answer."""
    if body.message.strip() == "":
        raise HTTPException(status_code=400, detail="The message is empty. Please type a request.")
    return handle_request(body.message)


@app.get("/bookings")
def get_bookings():
    """Return all bookings from bookings.json."""
    return tools.load_bookings()


@app.get("/health")
def get_health():
    """Simple check that the back end is running."""
    return {"status": "ok"}
