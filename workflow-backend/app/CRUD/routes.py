from fastapi import APIRouter
from schemas import CreateWorkflowRequest, CreateWorkflowResponse, Signup
from database import insert_workflow, get_all_workflows, get_workflow_by_id, update_workflow, delete_workflow
import datetime
import uuid

router = APIRouter()

# @router.post("/user/sign_up")
# async def sign_up(req: Signup):
#     userData = {
#         "userid": str(req.userid),
#         "username": req.username,
#         "email": req.email,
#         "password": req.password
#     }
#     return {"message": "User signed up successfully", "data": userData}

@router.post("/workflow/create/blank")
async def create_workflow(request: CreateWorkflowRequest):
    workflow_data = {
        "id": str(uuid.uuid4()),
        "name": request.name,
        "description": request.description,
        "status": "temp",
        "created_at": str(datetime.datetime.now()),
        "updated_at": str(datetime.datetime.now()),
        "created_by": str(request.user)
    }
    insert_workflow(workflow_data)
    return {"message": "Workflow created successfully", "workflow": workflow_data}

@router.get("/workflow/all_workflows")
async def fetch_all_workflows():
    workflows = get_all_workflows()
    return workflows

@router.get("/workflow/{workflow_id}")
async def fetch_workflow(workflow_id: str):
    workflow = get_workflow_by_id(workflow_id)
    return workflow if workflow else {"error": "Workflow not found"}

@router.put("/workflow/{workflow_id}")
async def modify_workflow(workflow_id: str, request: CreateWorkflowRequest):
    updated_data = {
        "name": request.name,
        "description": request.description,
        "updated_at": str(datetime.datetime.now())
    }
    updated_workflow = update_workflow(workflow_id, updated_data)
    return updated_workflow if updated_workflow else {"error": "Update failed"}

@router.delete("/workflow/{workflow_id}")
async def remove_workflow(workflow_id: str):
    deleted_workflow = delete_workflow(workflow_id)
    return deleted_workflow if deleted_workflow else {"error": "Deletion failed"}

