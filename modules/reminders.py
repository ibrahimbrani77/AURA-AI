from modules.database import SessionLocal
from modules.models import Reminder
import datetime

def create_reminder(title, due_date, user_id):
    db = SessionLocal()
    reminder = Reminder(title=title, due_date=due_date, user_id=user_id)
    db.add(reminder)
    db.commit()
    db.close()
    return True

def get_reminders(user_id):
    db = SessionLocal()
    reminders = db.query(Reminder).filter(
        Reminder.user_id == user_id,
        Reminder.done == 0
    ).order_by(Reminder.due_date).all()
    db.close()
    return reminders

def complete_reminder(reminder_id):
    db = SessionLocal()
    r = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if r:
        r.done = 1
        db.commit()
    db.close()

def delete_reminder(reminder_id):
    db = SessionLocal()
    r = db.query(Reminder).filter(Reminder.id == reminder_id).first()
    if r:
        db.delete(r)
        db.commit()
    db.close()

def get_overdue_reminders(user_id):
    db = SessionLocal()
    now = datetime.datetime.now()
    reminders = db.query(Reminder).filter(
        Reminder.user_id == user_id,
        Reminder.done == 0,
        Reminder.due_date < now
    ).all()
    db.close()
    return reminders
