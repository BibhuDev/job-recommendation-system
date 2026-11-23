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
    try:
        result = agent.invoke({
            "messages": [
                HumanMessage(content=request.message)
            ]
        })

        response_message = result["messages"][-1]

        return AgentChatResponse(
            response=response_message.content
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Agent execution failed: {str(error)}"
        )