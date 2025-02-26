import uuid

from fastapi import APIRouter, HTTPException
from app.schemas.workflow import WorkflowCreate, WorkflowResponse, WorkflowUpdate, ExecutionStatus
from app.crud.workflow import (
    create_workflow, get_workflow, update_workflow, delete_workflow,
    start_workflow_execution, get_execution_status, retry_execution
)

router = APIRouter()

@router.post("/create", response_model=WorkflowResponse)
async def create_new_workflow(workflow: WorkflowCreate):
    # print(workflow)
    return await create_workflow(workflow)



@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def read_workflow(workflow_id: uuid.UUID):
    workflow = await get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow

@router.put("/{workflow_id}", response_model=dict)
async def update_existing_workflow(workflow_id: uuid.UUID, workflow: WorkflowUpdate):
    await update_workflow(workflow_id, workflow)
    return {"message": "Workflow saved successfully"}

@router.delete("/{workflow_id}", response_model=dict)
async def delete_existing_workflow(workflow_id: uuid.UUID):
    await delete_workflow(workflow_id)
    return {"message": "workflow deleted successfully"}

@router.post("/{workflow_id}/start", response_model=dict)
async def start_workflow(workflow_id: uuid.UUID):
    result = await start_workflow_execution(workflow_id)
    return result

@router.get("/{workflow_id}/executions/{execution_id}/status", response_model=ExecutionStatus)
async def check_execution_status(workflow_id: uuid.UUID, execution_id: uuid.UUID):
    status = await get_execution_status(workflow_id, execution_id)
    return {"message": status}

@router.post("/{workflow_id}/executions/{execution_id}/retry", response_model=dict)
async def retry_workflow(workflow_id: uuid.UUID, execution_id: uuid.UUID):
    result = await retry_execution(workflow_id, execution_id)
    return result
