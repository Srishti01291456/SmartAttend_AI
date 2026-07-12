import cv2
import os
from database import add_student


# -----------------------------
# Project Paths
# -----------------------------

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


CASCADE_PATH = os.path.join(
    BASE_DIR,
    "models",
    "haarcascade_frontalface_default.xml"
)


# -----------------------------
# Load Face Detector
# -----------------------------

face_detector = cv2.CascadeClassifier(
    CASCADE_PATH
)


if face_detector.empty():
    print("❌ Haar Cascade not loaded")
    exit()


# -----------------------------
# Student Details
# -----------------------------

student_id = input("Enter Student ID: ")
student_name = input("Enter Student Name: ")


registered = add_student(
    student_id,
    student_name
)


if not registered:
    exit()


# -----------------------------
# Create Dataset Folder
# -----------------------------

dataset_path = os.path.join(
    BASE_DIR,
    "dataset",
    "students",
    f"{student_id}_{student_name}"
)


os.makedirs(
    dataset_path,
    exist_ok=True
)


print("\nStudent Registration Started")
print("Look at the camera...")


# -----------------------------
# Open Webcam
# -----------------------------

camera = cv2.VideoCapture(0)

count = 0


while True:

    ret, frame = camera.read()

    if not ret:
        print("❌ Camera error")
        break


    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )


    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5
    )


    for (x,y,w,h) in faces:

        count += 1


        face = gray[y:y+h, x:x+w]


        filename = os.path.join(
            dataset_path,
            f"{count}.jpg"
        )


        cv2.imwrite(
            filename,
            face
        )


        cv2.rectangle(
            frame,
            (x,y),
            (x+w,y+h),
            (255,0,0),
            2
        )


        cv2.putText(
            frame,
            f"Images: {count}/100",
            (x,y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255,255,255),
            2
        )


    cv2.imshow(
        "Register Student",
        frame
    )


    if count >= 100:
        print("✅ Dataset created successfully")
        break


    if cv2.waitKey(1) & 0xFF == ord('q'):
        break



camera.release()
cv2.destroyAllWindows()