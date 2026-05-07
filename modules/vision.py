import numpy as np
import cv2
from deepface import DeepFace


def capture_face_embedding(image_bytes):
    """
    Accepts raw bytes from st.camera_input (or .getvalue() buffer).
    Decodes into an OpenCV frame and extracts a face embedding via DeepFace.
    Returns the embedding as a string, or None on failure.

    Why NOT cv2.VideoCapture(0):
      VideoCapture(0) opens the HOST machine's webcam — i.e. the server.
      On Streamlit Cloud there is no webcam attached to the server, so it
      returns an empty/black frame immediately and the whole pipeline fails.
      st.camera_input captures from the CLIENT's browser camera and passes
      the JPEG bytes back to Python, so we decode those bytes here instead.
    """
    if image_bytes is None:
        return None
    try:
        # Support both raw bytes and file-like objects (UploadedFile)
        raw = image_bytes if isinstance(image_bytes, (bytes, bytearray)) else image_bytes.read()
        file_bytes = np.asarray(bytearray(raw), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if frame is None:
            print("capture_face_embedding: cv2.imdecode returned None — bad image bytes")
            return None

        embedding = DeepFace.represent(
            frame,
            model_name="SFace",
            enforce_detection=False
        )
        return str(embedding[0]["embedding"])

    except Exception as e:
        print(f"capture_face_embedding error: {e}")
        return None


def verify_face(stored_embedding, image_bytes):
    """
    Accepts the stored embedding string from the DB and raw bytes from
    st.camera_input. Decodes the image, extracts the live embedding,
    then computes cosine similarity against the stored one.
    Returns True if similarity >= 0.50, False otherwise.
    """
    if image_bytes is None or stored_embedding is None:
        return False
    try:
        # Decode incoming image
        raw = image_bytes if isinstance(image_bytes, (bytes, bytearray)) else image_bytes.read()
        file_bytes = np.asarray(bytearray(raw), dtype=np.uint8)
        frame = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if frame is None:
            print("verify_face: cv2.imdecode returned None — bad image bytes")
            return False

        # Get live embedding
        current = DeepFace.represent(
            frame,
            model_name="SFace",
            enforce_detection=False
        )
        current_emb = np.array(current[0]["embedding"])

        # Parse stored embedding (saved as a Python list string)
        stored_emb = np.array(eval(stored_embedding))

        # Cosine similarity
        norm_product = np.linalg.norm(current_emb) * np.linalg.norm(stored_emb)
        if norm_product == 0:
            return False

        cosine = np.dot(current_emb, stored_emb) / norm_product
        print(f"verify_face similarity: {cosine:.4f}")
        return float(cosine) >= 0.50

    except Exception as e:
        print(f"verify_face error: {e}")
        return False