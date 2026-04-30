from modules.database import SessionLocal 
from modules.models import Task

def create_task(title, desc, uid):
    db = SessionLocal()
    try:
        new = Task(title=title, description=desc, user_id=uid)
        db.add(new); db.commit(); return True
    except: db.rollback(); return False
    finally: db.close()


def get_tasks(uid):
    db = SessionLocal()
    try: 
        return db.query(Task).filter(Task.user_id == uid).order_by(Task.id.desc()).all()
    finally: db.close()


def complete_task(tid):
    db = SessionLocal()
    try:
        t = db.query(Task).filter(Task.id == tid).first()
        if t: 
            t.status = "completed"
            db.commit()
            return True
    finally: db.close()


# =========================
# NEW FUNCTION (DELETE TASK)
# =========================
def delete_task(tid):
    db = SessionLocal()
    try:
        t = db.query(Task).filter(Task.id == tid).first()
        if t:
            db.delete(t)
            db.commit()
            return True
    except:
        db.rollback()
        return False
    finally:
        db.close()