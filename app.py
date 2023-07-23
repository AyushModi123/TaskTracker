from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from user_model import Task, TasksList, TaskIds
from user_schema import tasks_ids_serializer, task_serializer_out, tasks_serializer_out
from bson.objectid import ObjectId
import uvicorn
import os
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
client = MongoClient(os.getenv('MONGODB_URL'))
db = client["waterdip_assignmentdb"]
collection = db["tasks"]

@app.post("/v1/tasks/")
async def create_task(task: Task):
    task_data = dict(task)
    _id = collection.insert_one(task_data).inserted_id
    posted_task_id = task_serializer_out(collection.find_one({"_id":ObjectId(_id)}))["id"]
    return JSONResponse(content={"id": posted_task_id}, status_code=201)

@app.get("/v1/tasks/")
async def list_tasks():
    all_tasks = tasks_serializer_out(collection.find())
    return JSONResponse(content = all_tasks, status_code=200)

@app.get("/v1/tasks/{task_id}")
async def get_task(task_id: str):
    task = collection.find_one({"_id": ObjectId(task_id)})    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    task = task_serializer_out(task)
    return JSONResponse(content = task, status_code=200)

@app.delete("/v1/tasks/{task_id}")
async def delete_task(task_id: str):
    task = collection.find_one({"_id": ObjectId(task_id)})
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    collection.delete_one({"_id": ObjectId(task_id)})
    return JSONResponse(content = None, status_code=204)

@app.put("/v1/tasks/{task_id}")
async def update_task(task_id: str, task: Task):
    task_data = dict(task)
    task_in_db = collection.find_one({"_id": ObjectId(task_id)})
    if not task_in_db:
        raise HTTPException(status_code=404, detail="Task not found")
    collection.update_one({"_id": ObjectId(task_id)}, {"$set": task_data})
    task_in_db =task_serializer_out(collection.find_one({"_id": ObjectId(task_id)}))
    return JSONResponse(content = None, status_code=204)

@app.post("/v1/tasks/bulk")
async def bulk_create_tasks(tasks: TasksList):    
    tasks_data = [dict(task) for task in tasks.tasks]
    _ids = collection.insert_many(tasks_data).inserted_ids
    _ids = tasks_ids_serializer(_ids)
    return JSONResponse(content={'tasks': _ids}, status_code=204)

@app.post("/v1/tasks/bulk_delete")
async def bulk_delete_tasks(task_ids: TaskIds):
    task_ids = [ObjectId(task_id["id"]) for task_id in task_ids.tasks]    
    collection.delete_many({"_id": {"$in": task_ids}})
    return JSONResponse(content = None, status_code=204)

if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True)