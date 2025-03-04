import uuid

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends

from app.schemas.workflow import WorkflowCreate, WorkflowResponse, DSL, ExecutionStatus, FileText
from app.crud.workflow import (
    create_workflow, get_workflow, get_all_workflows, update_dsl, delete_workflow,
    start_workflow_execution, get_execution_status, retry_execution, update_file_text
)
from app.core.security import get_current_user

router = APIRouter()

@router.post("/create", response_model=WorkflowResponse)
async def create_new_workflow(workflow: WorkflowCreate, current_user:uuid.UUID= Depends(get_current_user)):
    # print(workflow)
    print(current_user)
    return await create_workflow(workflow, current_user)

@router.get("/user/all", response_model=list[WorkflowResponse])
async def get_all_workflows_endpoint(user_id: uuid.UUID= Depends(get_current_user)):
    return await get_all_workflows(user_id)

@router.get("/{workflow_id}", response_model=WorkflowResponse)
async def read_workflow(workflow_id: uuid.UUID):
    workflow = await get_workflow(workflow_id)
    if not workflow:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflow


@router.post("/{workflow_id}/upload_file")
async def upload_text_endpoint(text: FileText, workflow_id: uuid.UUID):
    await update_file_text(workflow_id, text)
    return {"message": "File uploaded successfully"}

@router.post("/{workflow_id}/upload_dsl", response_model=dict)
async def update_existing_workflow(dsl: DSL, workflow_id: uuid.UUID):
    await update_dsl(workflow_id, dsl)
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
