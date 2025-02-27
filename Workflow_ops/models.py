from pydantic import BaseModel
import uuid

# Workflow Models
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

# User Signup Model
# class Signup(BaseModel):
#     userid: uuid.UUID
#     username: str
#     email: str
#     password: str

# Task Models (if needed)
class CreateTaskRequest(BaseModel):
    name: str
    description: str
'''
{
    "name": "workflow_1",
    "description": "this is a description for workflow_1"
}
'''

class TaskResponse(BaseModel):
    id: uuid.UUID
    workflow_id: uuid.UUID
    name: str
    description: str
    status: str
    created_at: str
    updated_at: str
    started_at: str | None = None

# Execution Models  
