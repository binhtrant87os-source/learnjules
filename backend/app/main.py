from fastapi import FastAPI

app = FastAPI(
    title="AI-Driven Assessment Platform",
    description="An automated platform for assessing embedded/automotive engineering candidates.",
    version="0.1.0",
)

@app.get("/")
async def root():
    return {"message": "Welcome to the AI-Driven Assessment Platform"}

@app.get("/health")
async def health_check():
    return {"status": "ok"}