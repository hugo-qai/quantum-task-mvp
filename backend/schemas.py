from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class TaskBase(BaseModel):
    title: String
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status: Optional[str] = "TODO"

class TaskCreate(TaskBase):
    pass

class SmartTaskCreate(BaseModel):
    raw_text: str

class TaskResponse(TaskBase):
    id: str
    priority_score: int
    smart_tags: List[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class SortedTasks(BaseModel):
    sorted_task_ids: List[str]
