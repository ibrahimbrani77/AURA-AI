import numpy as np
import cv2
from deepface import DeepFace


def capture_face_embedding(image_bytes):
    if image_bytes is None:
        return None
    try:
        raw = image_bytes if isinstance(image_bytes, (bytes, bytearray)) else image_bytes.read()
        file_bytes = np.asarray(bytearray(raw), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if frame is None:
            return None
        embedding = DeepFace.represent(frame, model_name="SFace", enforce_detection=False)
        return str(embedding[0]["embedding"])
    except Exception as e:
        print(f"capture_face_embedding error: {e}")
        return None


def verify_face(stored_embedding, image_bytes):
    if image_bytes is None or stored_embedding is None:
        return False
    try:
        raw = image_bytes if isinstance(image_bytes, (bytes, bytearray)) else image_bytes.read()
        file_bytes = np.asarray(bytearray(raw), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
        if frame is None:
            return False
        current = DeepFace.represent(frame, model_name="SFace", enforce_detection=False)
        current_emb = np.array(current[0]["embedding"])
        stored_emb = np.array(eval(stored_embedding))
        norm_product = np.linalg.norm(current_emb) * np.linalg.norm(stored_emb)
        if norm_product == 0:
            return False
        cosine = np.dot(current_emb, stored_emb) / norm_product
        return float(cosine) >= 0.50
    except Exception as e:
        print(f"verify_face error: {e}")
        return False