import os

IS_CLOUD = os.getenv("IS_CLOUD", "false").lower() == "true"

def capture_face_embedding():
    if IS_CLOUD:
        return None
    try:
        from deepface import DeepFace
        import cv2
        cap = cv2.VideoCapture(0)
        for _ in range(10):
            cap.read()
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return None
        embedding = DeepFace.represent(frame, model_name="SFace", enforce_detection=False)
        return str(embedding[0]["embedding"])
    except Exception as e:
        return None

def verify_face(stored_embedding):
    if IS_CLOUD:
        return False
    try:
        from deepface import DeepFace
        import cv2
        import numpy as np
        cap = cv2.VideoCapture(0)
        for _ in range(10):
            cap.read()
        ret, frame = cap.read()
        cap.release()
        if not ret:
            return False
        current = DeepFace.represent(frame, model_name="SFace", enforce_detection=False)
        current_emb = np.array(current[0]["embedding"])
        stored_emb  = np.array(eval(stored_embedding))
        cosine = np.dot(current_emb, stored_emb) / (
            np.linalg.norm(current_emb) * np.linalg.norm(stored_emb)
        )
        print(f"DEBUG similarity: {cosine}")
        return cosine >= 0.50
    except Exception as e:
        return False
