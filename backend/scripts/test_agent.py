from langchain_core.messages import HumanMessage

from backend.app.agents.graph import agent


def main():
    user_query = "Find Python backend internship jobs for someone with API development skills."

    response = agent.invoke({
        "messages": [
            HumanMessage(content=user_query)
        ]
    })

    print("\nUSER:")
    print(user_query)

    print("\nCAREERAI:")
    print(response["messages"][-1].content)


if __name__ == "__main__":
    main()