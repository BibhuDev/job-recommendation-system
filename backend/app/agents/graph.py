from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage
from langgraph.graph import StateGraph, START, MessagesState
from langgraph.prebuilt import ToolNode, tools_condition

from backend.app.core.config import settings
from backend.app.agents.tools import tools


if not settings.GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY is missing from .env")


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    api_key=settings.GROQ_API_KEY
)

llm_with_tools = llm.bind_tools(tools)


SYSTEM_PROMPT = """
You are CareerAI, an AI-powered job search assistant.

Your responsibilities:
1. Help users find relevant job opportunities.
2. Use the search_jobs tool whenever a user asks to find or search for jobs.
3. Use the actual search results when describing job opportunities.
4. Never invent job listings, companies, salaries, or application links.
5. If no matching jobs are found, clearly tell the user.
6. Present results in a clear, readable format.
7. Ask a follow-up question if the user's job search request is too vague.

You can search the available job database using the search_jobs tool.
"""


def assistant_node(state: MessagesState):
    messages = [
        SystemMessage(content=SYSTEM_PROMPT),
        *state["messages"]
    ]

    response = llm_with_tools.invoke(messages)

    return {"messages": [response]}


builder = StateGraph(MessagesState)

builder.add_node("assistant", assistant_node)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "assistant")

builder.add_conditional_edges(
    "assistant",
    tools_condition
)

builder.add_edge("tools", "assistant")

agent = builder.compile()