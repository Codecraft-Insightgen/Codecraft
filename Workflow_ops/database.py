import datetime
import uuid
from supabase_client import supabase
from uuid import UUID
# ---------------------
# Workflow Operations
# ---------------------
def insert_workflow(workflow_data: dict):
    response = supabase.table("workflows").insert(workflow_data).execute()
    return response

def get_all_workflows():
    response = supabase.table("workflows").select("*").execute()
    return response.data if response.data else []

def get_workflow_by_id(workflow_id: UUID):
    response = supabase.table("workflows").select("*").eq("id", workflow_id).execute()
    return response.data[0] if response.data else None

def update_workflow(workflow_id: str, updated_data: dict):
    response = supabase.table("workflows").update(updated_data).eq("id", workflow_id).execute()
    return response.data if response.data else None

def delete_workflow(workflow_id: str):
    response = supabase.table("workflows").delete().eq("id", workflow_id).execute()
    return response.data if response.data else None

# ---------------------
# Task Operations (if needed)
# ---------------------
def insert_task(task_data: dict):
    response = supabase.table("tasks").insert(task_data).execute()
    return response

def start_task(task_id: str):
    updated_data = {
        "status": "in_progress",
        "started_at": str(datetime.datetime.now()),
        "updated_at": str(datetime.datetime.now()),
    }
    response = supabase.table("tasks").update(updated_data).eq("id", task_id).execute()
    return response

def get_task_status(task_id: str):
    response = supabase.table("tasks").select("status").eq("id", task_id).execute()
    return response.data[0] if response.data else None

# ---------------------
# Workflow Execution & Logging
# ---------------------
def update_workflow_status(workflow_id: UUID, status: str):
    updated_data = {
        "status": status,
        "updated_at": str(datetime.datetime.now())
    }
    response = supabase.table("workflows").update(updated_data).eq("id", workflow_id).execute()
    return response.data if response.data else None

def add_workflow_log(workflow_id: UUID, log_message: str):
    log_data = {
        "id": str(uuid.uuid4()),
        "workflow_id": workflow_id,
        "log_message": log_message,
        "started_at": str(datetime.datetime.now())
    }
    response = supabase.table("workflow_logs").insert(log_data).execute()
    return response.data if response.data else None

def get_workflow_logs(workflow_id: str):
    response = supabase.table("workflow_logs").select("*").eq("workflow_id", workflow_id).execute()
    return response.data if response.data else []
