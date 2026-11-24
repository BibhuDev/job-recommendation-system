from typing import Optional

from pydantic import BaseModel, Field


class AgentChatRequest(BaseModel):
    message: str = Field(
        min_length=1,
        max_length=2000
    )
    thread_id: Optional[str] = Field(
        default=None,
        description="Conversation ID. Reuse it to continue a conversation."
    )


class AgentChatResponse(BaseModel):
    response: str
    thread_id: str