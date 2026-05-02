import cv2

print("Attempting to open camera...")
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
ret, frame = cam.read()

if ret:
    print("✅ Camera works perfectly! Frame captured.")
else:
    print("❌ Camera failed to open.")

cam.release()
