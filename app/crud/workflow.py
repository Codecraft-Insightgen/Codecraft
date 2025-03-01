from app.models.workflow import Workflow
from app.schemas.workflow import WorkflowCreate, DSL, FileText
from app.db.session import async_session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException
from sqlalchemy.future import select
from app.engine import engine
import datetime
import uuid

async def create_workflow(workflow: WorkflowCreate, current_user:uuid.UUID):
    async with async_session() as session:
        # print(current_user)
        # print(type(current_user))
        new_workflow = Workflow(
            workflow_name=workflow.workflow_name,
            description=workflow.description,
            created_by=current_user,
            dsl_file=workflow.dsl_file
        )
        try:
            session.add(new_workflow)
            await session.commit()
            await session.refresh(new_workflow)
            return new_workflow
        except IntegrityError:
            await session.rollback()
            raise HTTPException(
                status_code=400,
                detail="workflow name unavailable, choose a different workflow name"
            )

async def get_workflow(workflow_id: uuid.UUID):
    async with async_session() as session:
        result = await session.execute(select(Workflow).filter(Workflow.workflow_id == workflow_id))
        return result.scalars().first()

async def get_all_workflows(user_id):
    async with async_session() as session:
        result = await session.execute(select(Workflow).filter(Workflow.created_by == user_id))
        return result.scalars().all()

async def update_dsl(workflow_id: uuid.UUID, dsl: DSL):
    async with async_session() as session:
        result = await session.execute(select(Workflow).filter(Workflow.workflow_id == workflow_id))
        wf = result.scalars().first()
        if wf:
            wf.dsl_file = dsl
            wf.updated_at = datetime.datetime.now()
            await session.commit()

async def update_file_text(workflow_id: uuid.UUID, text: FileText):
    async with async_session() as session:
        result = await session.execute(select(Workflow).filter(Workflow.workflow_id == workflow_id))
        wf = result.scalars().first()
        if wf:
            wf.file_input_text = text
            await session.commit()

async def delete_workflow(workflow_id: uuid.UUID):
    async with async_session() as session:
        result = await session.execute(select(Workflow).filter(Workflow.workflow_id == workflow_id))
        wf = result.scalars().first()
        if wf:
            await session.delete(wf)
            await session.commit()

async def start_workflow_execution(workflow_id: uuid.UUID):
    # Simulate starting workflow execution and generating an execution ID
    async with async_session() as session:
        workflow = await session.execute(select(Workflow).filter(Workflow.workflow_id == workflow_id))
        wf = workflow.scalars().first()
        dsl_file = wf.dsl_file
        order = await engine.parse_and_get_order(dsl_file)
        await session.commit()
    return {"message": "Execution started", "execution_id": 123, "order": order}

async def get_execution_status(workflow_id: uuid.UUID, execution_id: uuid.UUID):
    # Simulate checking execution status
    return "50% completed"

async def retry_execution(workflow_id: uuid.UUID, execution_id: uuid.UUID):
    # Simulate retrying execution and generating new execution ID
    return {"message": "Retrying", "new_execution_id": 124}
