from modules.database import SessionLocal
from modules.models import Personalization

def save_preference(user_id, key, value):
    db = SessionLocal()
    existing = db.query(Personalization).filter(
        Personalization.user_id == user_id,
        Personalization.key == key
    ).first()
    if existing:
        existing.value = value
    else:
        db.add(Personalization(user_id=user_id, key=key, value=value))
    db.commit()
    db.close()

def get_preferences(user_id):
    db = SessionLocal()
    prefs = db.query(Personalization).filter(
        Personalization.user_id == user_id
    ).all()
    db.close()
    return {p.key: p.value for p in prefs}

def build_user_context(user_id):
    prefs = get_preferences(user_id)
    if not prefs:
        return ""
    parts = []
    if "name" in prefs:
        parts.append(f"User's name is {prefs['name']}")
    if "role" in prefs:
        parts.append(f"They work as {prefs['role']}")
    if "goals" in prefs:
        parts.append(f"Their goals are: {prefs['goals']}")
    if "preferences" in prefs:
        parts.append(f"Their preferences: {prefs['preferences']}")
    if "timezone" in prefs:
        parts.append(f"Timezone: {prefs['timezone']}")
    return ". ".join(parts)
