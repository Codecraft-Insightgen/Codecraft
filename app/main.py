from fastapi import FastAPI
from app.api.endpoints import workflows

app = FastAPI()

app.include_router(workflows.router, prefix="/workflows")

@app.get("/")
async def root():
    return {"message": "Welcome to CodeCraft API"}
