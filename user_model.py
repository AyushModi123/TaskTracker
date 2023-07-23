from pydantic import BaseModel
from typing import List, Dict
class Task(BaseModel):
    title: str
    is_completed: bool = False

class TasksList(BaseModel):
    tasks: List[Task]

class TaskIds(BaseModel):
    tasks: List[Dict[str, str]]

# class TaskOut(BaseModel):
#     _id : str = Field(alias="_id")
#     title: str
#     is_completed: bool  