import uuid
import uvicorn
from supabase_client import supabase
from fastapi import FastAPI
from pydantic import BaseModel
import datetime

app = FastAPI()

@app.get("/favicon.ico")
async def favicon():
    return {"message":"No Favicon"}

@app.get("/")
async def root():
    return {"message": "yes!"}

class CreateWorkflowRequest(BaseModel):
    user: uuid.UUID
    name: str
    description: str


class CreateWorkflowResponse(BaseModel):
    created_by : uuid.UUID
    id : uuid.UUID
    name: str
    description: str
    status: str
    created_at: str
    # createdAt: datetime.datetime
    updated_at: str
    # updatedAt: datetime.datetime

class Signup(BaseModel):
    userid: uuid.UUID
    username: str
    email : str
    password : str

@app.post("/workflow/create/blank")
async def create_workflow(request: CreateWorkflowRequest):
    try:
        workflow_data = {
            "name": request.name,
            "description": request.description,
            "status": "temp",
            "created_at": str(datetime.datetime.now()),
            "updated_at": str(datetime.datetime.now()),
            "created_by": str(request.user)
        }
        #add section for error handling #
        response = supabase.table("workflows").insert(workflow_data).execute()
        if response.error:
            return {"error": response.error.message}
        workflow = response[0]


        return {
            "message": "Successfully added workflow to Supabase.",
            "workflow": CreateWorkflowResponse(
                id=workflow["id"],
                name=workflow["name"],
                description=workflow["description"],
                status=workflow["status"],
                created_at=workflow["created_at"],
                updated_at=workflow["updated_at"],
                created_by=workflow["created_by"]
            )  # Convert the Pydantic model to a dictionary
        }
    except Exception as error:
        print(error)
        if(error.args[0][1:16])=="'code': '23505'":
            return {"error": "A workflow with this name already exists. Please enter a different name."}
        else:
            return error

@app.get("/workflow/all_workflows")
async def get_all_workflows():
    try:
        workflows = supabase.table("workflows").select("*").execute()
        if workflows.data:
            # print(workflows.data)
            return workflows
    except Exception as error:
        print(error)



@app.get("/workflow/workflow_id")
async def get_workflow(workflow_id: str):
    try:
        workflow = supabase.table("workflows").select("*").eq("name", workflow_id).execute()
        if workflow.data:
            return workflow.data[0]

    except Exception as error:
        print(error)


@app.get("/tools")
async def get_tools():
    try:
        tools = supabase.table("tools").select("*").execute()
        if tools.data:
            return tools
    except Exception as error:
        print(error)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)