# task-2-todo-api/models.py
from pydantic import BaseModel, EmailStr
from typing import Optional

# 1. User Models (For Sign Up & Login)
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# 2. Task Models (For creating/updating tasks)
class TaskModel(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None