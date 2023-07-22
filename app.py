from fastapi import FastAPI
# import pandas as pd
# import mysql.connector
from pymongo import MongoClient
import uvicorn
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
from bson import ObjectId
from typing import List, Union

class TaskInfo(BaseModel):
    title: str
    is_completed: bool = False

load_dotenv()
app = FastAPI()
MONGODB_URL = os.getenv('MONGODB_URL')

def MongoDB():
    client = MongoClient(MONGODB_URL)
    db_records = client.get_database('waterdip_assignmentdb')
    tasks_records = db_records.tasks
    return tasks_records


tasks_records = MongoDB()

    
origins = '*'

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/v1/tasks/")
async def add_tasks(tasks_info: Union[TaskInfo, List[TaskInfo]]):
    try:
        if isinstance(tasks_info, list):
            ids = tasks_records.insert_many(dict(tasks_info)).inserted_ids
            ids = [str(id) for id in ids]
            return {'id':ids}, 201
        else:
            id = tasks_records.insert_one(dict(tasks_info)).inserted_id
            return {'id':str(id)}, 201
    except Exception as e:
        print(e)
        return {'error':e}, 503
    
@app.get("/v1/tasks/")
async def get_tasks():
    all_tasks = [task for task in tasks_records.find()]
    return {'tasks' : all_tasks}, 200

@app.get("/v1/tasks/{id}")
async def get_tasks_by_id(id:str):
    task = tasks_records.find_one({"_id":ObjectId(id)}, {"title":1, "is_complete":1})
    if task:
        task['_id'] = str(task['_id'])
        return task, 200
    else:
        return {'error': '"There is no task at that id"'}, 404

if __name__ == '__main__':
    uvicorn.run("app:app", host="0.0.0.0", port=5000, reload=True)
