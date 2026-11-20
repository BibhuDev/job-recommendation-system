from fastapi import FastAPI

app = FastAPI(
    title="CareerAI",
    description="AI-Powered Job Search and Recommendation Agent"
)


@app.get("/")
def home():
    return {
        "message": "Welcome to CareerAI!",
        "status": "API is running"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
