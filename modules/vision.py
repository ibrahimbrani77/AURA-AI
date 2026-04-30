import cv2
import json
import numpy as np
from deepface import DeepFace
import time

def capture_face_embedding():
    """Captures a clear frame from webcam and returns the SFace embedding."""
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW) 
    
    # --- FIX 1: Camera Warmup ---
    # Throw away the first 10 frames to let the lens adjust lighting/focus
    for _ in range(10):
        cam.read()
        time.sleep(0.05)
        
    ret, frame = cam.read()
    cam.release()
    
    if not ret:
        print("Camera failed to grab frame.")
        return None

    try:
        embeddings = DeepFace.represent(frame, model_name="SFace", enforce_detection=True)
        return json.dumps(embeddings[0]["embedding"])
    except Exception as e:
        print(f"Face not detected: {e}")
        return None

def verify_face(stored_json):
    """Compares live face to the database face."""
    live_json = capture_face_embedding()
    if not live_json or not stored_json: 
        return False
        
    # Convert text back to math vectors
    s_vec = np.array(json.loads(stored_json))
    l_vec = np.array(json.loads(live_json))
    
    # --- FIX 2: The Math Threshold ---
    # Calculate Cosine Similarity (How close the vectors are)
    similarity = np.dot(s_vec, l_vec) / (np.linalg.norm(s_vec) * np.linalg.norm(l_vec))
    
    # Print the score in VS Code so you can see it!
    print(f"DEBUG - Face Similarity Score: {similarity:.3f}") 
    
    # 0.50 is the "sweet spot" for SFace. 
    # If it's too strict, lower it to 0.45. If anyone can log in, raise to 0.60.
    return similarity > 0.50