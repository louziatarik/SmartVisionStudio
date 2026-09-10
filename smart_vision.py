import cv2
import os
import time
from datetime import datetime

# ==========================================
# SMART VISION MONITOR
# AI Visual Perception - Face Detection
# ==========================================

# Create folder for screenshots
os.makedirs("captures", exist_ok=True)

# Load the pre-trained Haar Cascade face detection model
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)

# Check if the face detection model loaded correctly
if face_cascade.empty():
    print("Error: Could not load face detection model.")
    exit()

# Open the default webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# FPS calculation
previous_time = time.time()

# Used to detect changes in face status
previous_face_count = 0

# Screenshot counter
capture_number = 1

print("==========================================")
print("       SMART VISION MONITOR")
print("==========================================")
print("Camera: ONLINE")
print("Press S = Save Screenshot")
print("Press Q = Quit")
print("==========================================")

while True:

    # Read a frame from the camera
    ret, frame = cap.read()

    if not ret:
        print("Error: Could not read frame.")
        break

    # Calculate FPS
    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30)
    )

    face_count = len(faces)

    # Draw green rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(
            frame,
            (x, y),
            (x + w, y + h),
            (0, 255, 0),
            2
        )

    # Detection status
    if face_count > 0:
        detection_status = "FACE DETECTED"
    else:
        detection_status = "NO FACE"

    # Log detection events when the number of faces changes
    if face_count != previous_face_count:

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if face_count > 0:
            log_message = f"{timestamp} - Face detected ({face_count})"
        else:
            log_message = f"{timestamp} - No face detected"

        with open("detection_log.txt", "a") as log_file:
            log_file.write(log_message + "\n")

        previous_face_count = face_count

    # Current timestamp
    timestamp_display = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Display face count
    cv2.putText(
        frame,
        f"Faces: {face_count}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        (0, 255, 0),
        2
    )

    # Display FPS
    cv2.putText(
        frame,
        f"FPS: {fps:.1f}",
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    # Display camera status
    cv2.putText(
        frame,
        "Camera: ONLINE",
        (20, 105),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    # Display detection status
    cv2.putText(
        frame,
        f"Status: {detection_status}",
        (20, 140),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 0),
        2
    )

    # Display timestamp
    cv2.putText(
        frame,
        timestamp_display,
        (20, 175),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    # Display keyboard instructions
    cv2.putText(
        frame,
        "S: Save Screenshot | Q: Quit",
        (20, frame.shape[0] - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    # Show the camera
    cv2.imshow(
        "Smart Vision Monitor",
        frame
    )

    # Read keyboard input
    key = cv2.waitKey(1) & 0xFF

    # Press S to save screenshot
    if key == ord("s"):

        filename = f"captures/detection_{capture_number:03d}.jpg"

        cv2.imwrite(filename, frame)

        print(f"Screenshot saved: {filename}")

        capture_number += 1

    # Press Q to quit
    elif key == ord("q"):
        break

# Release camera
cap.release()

# Close OpenCV windows
cv2.destroyAllWindows()

print("==========================================")
print("Smart Vision Monitor stopped.")
print("==========================================")