import uuid
import datetime
from fastapi import APIRouter, HTTPException
from models import (
    CreateWorkflowRequest,
    CreateWorkflowResponse,
    #Signup,
    CreateTaskRequest,
    TaskResponse,
)
from database import (
    insert_workflow,
    get_all_workflows,
    get_workflow_by_id,
    update_workflow,
    delete_workflow,
    insert_task,
    start_task,
    get_task_status,
    update_workflow_status,
    add_workflow_log,
    get_workflow_logs,
)
from supabase_client import supabase  # For user signup endpoint
from uuid import UUID

router = APIRouter()

def make_json_serializable(data):
    """
    Recursively convert UUIDs and other non-serializable objects to JSON-compatible types.
    """
    if isinstance(data, dict):
        return {key: make_json_serializable(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [make_json_serializable(item) for item in data]
    elif isinstance(data, UUID):
        return str(data)  # Convert UUID to string
    return data  # Return other types as-is


# ---------------------
# User Endpoints
# ---------------------
# @router.post("/user/sign_up")
# async def sign_up(req: Signup):
#     user_data = {
#         "userid": str(req.userid),
#         "username": req.username,
#         "email": req.email,
#         "password": req.password,
#     }
#     response = supabase.table("users").insert(user_data).execute()
#     if response.error:
#         raise HTTPException(status_code=400, detail=response.error.message)
#     return {"message": "User registered successfully.", "data": user_data}

# ---------------------
# Workflow Endpoints
# ---------------------
@router.post("/workflow/create/blank", response_model=CreateWorkflowResponse)
async def create_workflow(request: CreateWorkflowRequest):
    workflow_data = {
        "id": str(uuid.uuid4()),
        "name": request.name,
        "description": request.description,
        "status": "temp",
        "created_at": str(datetime.datetime.now()),
        "updated_at": str(datetime.datetime.now()),
        "created_by": str(request.user),
    }
    response = insert_workflow(workflow_data)
    if response.error:
        if response.error.message.startswith("duplicate key value violates"):
            raise HTTPException(
                status_code=400,
                detail="A workflow with this name already exists. Please choose a different name.",
            )
        raise HTTPException(status_code=400, detail=response.error.message)
    return CreateWorkflowResponse(
        id=uuid.UUID(workflow_data["id"]),
        name=workflow_data["name"],
        description=workflow_data["description"],
        status=workflow_data["status"],
        created_at=workflow_data["created_at"],
        updated_at=workflow_data["updated_at"],
        created_by=uuid.UUID(workflow_data["created_by"]),
    )

@router.get("/workflow/all_workflows")
async def fetch_all_workflows():
    workflows = get_all_workflows()
    return {"workflows": workflows}

@router.get("/workflow/{workflow_id}")
async def fetch_workflow(workflow_id: str):
    workflow = get_workflow_by_id(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {"workflow": workflow}

@router.put("/workflow/{workflow_id}")
async def modify_workflow(workflow_id: str, request: CreateWorkflowRequest):
    updated_data = {
        "name": request.name,
        "description": request.description,
        "updated_at": str(datetime.datetime.now()),
    }
    updated_workflow = update_workflow(workflow_id, updated_data)
    if not updated_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found or update failed")
    return {"message": "Workflow updated successfully.", "updated_workflow": updated_workflow}

@router.delete("/workflow/{workflow_id}")
async def remove_workflow(workflow_id: str):
    deleted_workflow = delete_workflow(workflow_id)
    if not deleted_workflow:
        raise HTTPException(status_code=404, detail="Workflow not found or deletion failed")
    return {"message": "Workflow deleted successfully."}

# ---------------------
# Task Endpoints
# ---------------------
@router.post("/workflow/{workflow_id}/tasks/add")
async def add_task(workflow_id: str, request: CreateTaskRequest):
    task_data = {
        "id": str(uuid.uuid4()),
        "workflow_id": workflow_id,
        "name": request.name,
        "description": request.description,
        "status": "pending",
        "created_at": str(datetime.datetime.now()),
        "updated_at": str(datetime.datetime.now()),

    }
    response = insert_task(task_data)
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    return {"message": "Task added successfully", "task": task_data}

@router.post("/tasks/{task_id}/start")
async def start_task_endpoint(task_id: str):
    response = start_task(task_id)
    if response.error:
        raise HTTPException(status_code=400, detail=response.error.message)
    if not response.data:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task started successfully", "task": response.data[0]}

@router.get("/tasks/{task_id}/status")
async def task_status(task_id: str):
    task = get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"task_id": task_id, "status": task["status"]}

# ---------------------
# Workflow Execution Endpoints
# ---------------------
@router.post("/workflow/{workflow_id}/start")
async def start_workflow(workflow_id: str):
    workflow = get_workflow_by_id(workflow_id)
    if not workflow:
        # Log error to the log table
        add_workflow_log(workflow_id, "Workflow not found when attempting to start execution")
        raise HTTPException(status_code=404, detail="Workflow not found")
    updated = update_workflow_status(workflow_id, "in_progress")
    if not updated:
        # Log failure to start
        add_workflow_log(workflow_id, "Failed to start workflow")
        raise HTTPException(status_code=400, detail="Failed to start workflow")
    # Log the start event in the separate log table
    log = add_workflow_log(workflow_id, "Workflow execution started")
    return {"message": "Workflow execution started", "workflow": updated[0], "log": log}

@router.post("/workflow/{workflow_id}/retry")
async def retry_workflow(workflow_id: str):
    workflow = get_workflow_by_id(workflow_id)
    if not workflow:
        add_workflow_log(workflow_id, "Workflow not found during retry attempt")
        raise HTTPException(status_code=404, detail="Workflow not found")
    updated = update_workflow_status(workflow_id, "in_progress")
    if not updated:
        add_workflow_log(workflow_id, "Failed to retry workflow")
        raise HTTPException(status_code=400, detail="Failed to retry workflow")
    log = add_workflow_log(workflow_id, "Workflow retried execution")
    return {"message": "Workflow retried successfully", "workflow": updated[0], "log": log}

@router.get("/workflow/{workflow_id}/status")
async def workflow_status(workflow_id: str):
    workflow = get_workflow_by_id(workflow_id)
    if not workflow:
        add_workflow_log(workflow_id, "Workflow status requested but workflow not found")
        raise HTTPException(status_code=404, detail="Workflow not found")
    return {"workflow_id": workflow_id, "status": workflow.get("status")}

@router.get("/workflow/{workflow_id}/logs")
async def workflow_logs(workflow_id: str):
    logs = get_workflow_logs(workflow_id)
    return {"workflow_id": workflow_id, "logs": logs}

# Python logger