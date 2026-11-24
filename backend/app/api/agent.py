from uuid import uuid4

from fastapi import APIRouter, HTTPException
from langchain_core.messages import HumanMessage

from backend.app.agents.graph import agent
from backend.app.schemas.agent import (
    AgentChatRequest,
    AgentChatResponse
)

router = APIRouter(
    prefix="/agent",
    tags=["AI Agent"]
)


@router.post("/chat", response_model=AgentChatResponse)
def chat_with_agent(request: AgentChatRequest):
    thread_id = request.thread_id or str(uuid4())

    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    try:
        result = agent.invoke(
            {
                "messages": [
                    HumanMessage(content=request.message)
                ]
            },
            config=config
        )

        response_message = result["messages"][-1]

        return AgentChatResponse(
            response=response_message.content,
            thread_id=thread_id
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="Agent execution failed. Check the backend logs."
        )