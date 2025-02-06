from pydantic import BaseModel
import uuid

class CreateWorkflowRequest(BaseModel):
    user: uuid.UUID
    name: str
    description: str

class CreateWorkflowResponse(BaseModel):
    created_by: uuid.UUID
    id: uuid.UUID
    name: str
    description: str
    status: str
    created_at: str
    updated_at: str

class Signup(BaseModel):
    userid: uuid.UUID
    username: str
    email: str
    password: str
