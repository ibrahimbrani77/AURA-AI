from modules.database import SessionLocal
from modules.models import Note

def create_note(title, content, user_id):
    db = SessionLocal()
    new_note = Note(title=title, content=content, user_id=user_id)
    db.add(new_note)
    db.commit()
    db.close()
    return True

def get_notes(user_id):
    db = SessionLocal()
    notes = db.query(Note).filter(Note.user_id == user_id).all()
    db.close()
    return notes

def delete_note(note_id):
    db = SessionLocal()
    n = db.query(Note).filter(Note.id == note_id).first()
    if n:
        db.delete(n)
        db.commit()
    db.close()