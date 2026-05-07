import os

import face_recognition
import numpy as np
from PIL import Image
import io

def capture_face_embedding(image_bytes):
    """
    Takes an image buffer from st.camera_input and returns the face embedding.
    """
    if image_bytes is None:
        return None
        
    try:
        # face_recognition can load directly from a file-like object (the Streamlit bytes)
        image = face_recognition.load_image_file(image_bytes)
        
        # Find face encodings
        encodings = face_recognition.face_encodings(image)
        
        # If at least one face is found, return the first one
        if len(encodings) > 0:
            # We convert it to a string or bytes depending on how your database saves it.
            # Usually, storing it as a byte array or list is standard.
            return encodings[0].tobytes() 
        else:
            return None
            
    except Exception as e:
        print(f"Error capturing face: {e}")
        return None

def verify_face(stored_embedding, image_bytes):
    """
    Compares a stored embedding against a new image buffer from st.camera_input.
    """
    if image_bytes is None or stored_embedding is None:
        return False
        
    try:
        # Load the new image from Streamlit
        image = face_recognition.load_image_file(image_bytes)
        unknown_encodings = face_recognition.face_encodings(image)
        
        if len(unknown_encodings) > 0:
            # Convert the stored embedding back to a numpy array if it was saved as bytes
            known_encoding = np.frombuffer(stored_embedding)
            
            # Compare faces (returns a list of booleans)
            results = face_recognition.compare_faces([known_encoding], unknown_encodings[0])
            
            return results[0] # True if match, False if not
        else:
            return False
            
    except Exception as e:
        print(f"Error verifying face: {e}")
        return False