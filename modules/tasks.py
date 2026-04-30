from modules.database import SessionLocal
from modules.models import Task

def create_task(title, description, user_id, priority="Medium"):
    db = SessionLocal()
    task = Task(title=title, description=description, user_id=user_id, priority=priority)
    db.add(task)
    db.commit()
    db.close()
    return True

def get_tasks(user_id):
    db = SessionLocal()
    tasks = db.query(Task).filter(Task.user_id == user_id).all()
    db.close()
    return tasks

def complete_task(task_id):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        task.status = "completed"
        db.commit()
    db.close()

def delete_task(task_id):
    db = SessionLocal()
    task = db.query(Task).filter(Task.id == task_id).first()
    if task:
        db.delete(task)
        db.commit()
    db.close()