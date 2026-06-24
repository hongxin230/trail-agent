from fastapi import FastAPI
from pydantic import BaseModel

from graph.graph import build_graph

app = FastAPI()

graph = build_graph()


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(req: ChatRequest):

    result = graph.invoke({
        "user_input": req.message,
        "intent": "",
        "response": ""
    })

    return {
        "intent": result["intent"],
        "response": result["response"]
    }