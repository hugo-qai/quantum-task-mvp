from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas, nlp
from database import engine, get_db
import uuid

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="QuantumTask API")

@app.post("/tasks/smart-create", response_model=schemas.TaskResponse)
def smart_create_task(request: schemas.SmartTaskCreate, db: Session = Depends(get_db)):
    # 1. Parse NLP
    parsed = nlp.parse_task_nlp(request.raw_text)
    
    # 2. Create Task
    # TODO: user_id hardcoded for MVP
    task = models.Task(
        title=parsed["title"],
        raw_nlp_input=request.raw_text,
        due_date=parsed["due_date"],
        priority_score=parsed["predicted_priority"],
        smart_tags=parsed["smart_tags"],
        user_id="demo-user" 
    )
    
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@app.get("/tasks", response_model=List[schemas.TaskResponse])
def get_tasks(db: Session = Depends(get_db)):
    return db.query(models.Task).all()

@app.get("/tasks/quantum-sort", response_model=schemas.SortedTasks)
def get_sorted_tasks(db: Session = Depends(get_db)):
    tasks = db.query(models.Task).filter(models.Task.status != "DONE").all()
    
    # Sort by quantum score
    # In real app, we'd update scores first
    sorted_tasks = sorted(tasks, key=lambda t: nlp.calculate_quantum_score(t), reverse=True)
    
    return {"sorted_task_ids": [t.id for t in sorted_tasks]}
