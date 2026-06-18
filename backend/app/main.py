from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "status": "running",
        "project": "Enterprise AI Workspace"
    }