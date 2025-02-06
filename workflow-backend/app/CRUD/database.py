from supabase_client import supabase

def insert_workflow(workflow_data):
    response = supabase.table("workflows").insert(workflow_data).execute()
    return response

def get_all_workflows():
    response = supabase.table("workflows").select("*").execute()
    return response.data if response.data else []

def get_workflow_by_id(workflow_id):
    response = supabase.table("workflows").select("*").eq("id", workflow_id).execute()
    return response.data[0] if response.data else None

def update_workflow(workflow_id, updated_data):
    response = supabase.table("workflows").update(updated_data).eq("id", workflow_id).execute()
    return response.data if response.data else None

def delete_workflow(workflow_id):
    response = supabase.table("workflows").delete().eq("id", workflow_id).execute()
    return response.data if response.data else None
