from fastapi import FastAPI
from app.api.endpoints import workflows, auth
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:3000",
    # Add any other domains as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,            # Allowed origins
    allow_credentials=True,           # Allow cookies, authorization headers, etc.
    allow_methods=["*"],              # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # Allow all headers
)
app.include_router(workflows.router, prefix="/workflows")
app.include_router(auth.router, prefix="/auth")

@app.get("/")
async def root():
    return {"message": "Welcome to CodeCraft API"}
