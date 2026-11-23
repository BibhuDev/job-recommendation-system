
from langchain_groq import ChatGroq
from backend.app.core.config import settings


def main():
    if not settings.GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY is missing from .env")

    llm = ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0,
        api_key=settings.GROQ_API_KEY
    )

    response = llm.invoke(
        "Explain what a job recommendation system does in two sentences."
    )

    print("Groq connection successful!")
    print(response.content)


if __name__ == "__main__":
    main()
