import hashlib
from datetime import datetime, timedelta
import jwt
import passlib.context
import os
from sqlalchemy.orm import Session
from modules.database import SessionLocal
from modules.models import User

# --- 1. Security Configurations ---
SECRET_KEY = os.getenv("JWT_SECRET", "super-secure-graduation-key-2026")
ALGORITHM = "HS256"

# EXPERT FIX: Using pbkdf2_sha256 instead of bcrypt to avoid the 72-character limit
# and the passlib initialization bug.
pwd_context = passlib.context.CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# --- 2. Password Security ---

def hash_password(password: str) -> str:
    """Hashes a password using PBKDF2 (No length limits)."""
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    """Verifies a password against the stored PBKDF2 hash."""
    if not hashed:
        return False
    return pwd_context.verify(password, hashed)

# --- 3. User Operations ---

def register_user(name, email, password, face_embedding=None):
    """تسجيل مستخدم جديد في قاعدة البيانات."""
    db = SessionLocal()
    try:
        existing_user = db.query(User).filter(User.email == email).first()
        if existing_user:
            return None

        new_user = User(
            name=name,
            email=email,
            password_hash=hash_password(password),
            face_embedding=face_embedding
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        db.rollback()
        print(f"❌ Error during registration: {e}")
        return None
    finally:
        db.close()

def login_user(email, password):
    """تسجيل الدخول التقليدي وإعادة توكن JWT."""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if user and verify_password(password, user.password_hash):
            return create_token({"id": user.id, "email": user.email})
        return None
    finally:
        db.close()

def get_user_by_email(email):
    """البحث عن مستخدم بالبريد الإلكتروني."""
    db = SessionLocal()
    try:
        return db.query(User).filter(User.email == email).first()
    finally:
        db.close()

def login_user_biometric(email):
    """تسجيل الدخول عبر بصمة الوجه."""
    user = get_user_by_email(email)
    if user:
        return create_token({"id": user.id, "email": user.email})
    return None

# --- 4. JWT Handling ---

def create_token(user_data: dict):
    """إنشاء توكن JWT بصلاحية 24 ساعة."""
    payload = {
        "user_id": user_data["id"],
        "email": user_data["email"],
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    """فك تشفير التوكن والتحقق من صلاحيته."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.ExpiredSignatureError:
        print("⚠️ Session Expired")
        return None
    except jwt.InvalidTokenError:
        print("❌ Invalid Token")
        return None
