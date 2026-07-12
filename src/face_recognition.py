import cv2
import time

from database import load_students
from attendance import mark_attendance

students = load_students()

marked_today = set()

attendance_status = ""
status_time = 0

face_detector = cv2.CascadeClassifier(
    "models/haarcascade_frontalface_default.xml"
)

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainer/trainer.yml")

camera = cv2.VideoCapture(0)

while True:

    ret, frame = camera.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(100, 100)
    )

    for (x, y, w, h) in faces:

        face = gray[y:y+h, x:x+w]

        # Resize exactly like training images
        face = cv2.resize(face, (200, 200))

        student_id, conf = recognizer.predict(face)

        confidence = round(100 - conf)

        if confidence >= 40:

            name = students.get(str(student_id), "Unknown")
            color = (0, 255, 0)

            if student_id not in marked_today:

                status = mark_attendance(student_id, name)

                if status == "Attendance Marked":
                    attendance_status = f"Attendance Marked: {name}"
                else:
                    attendance_status = "Attendance Already Marked Today"

                marked_today.add(student_id)

            status_time = time.time()

        else:

            name = "Unknown"
            color = (0, 0, 255)

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            color,
            2
        )

        cv2.putText(
            frame,
            name,
            (x, y-10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            color,
            2
        )

        cv2.putText(
            frame,
            f"Confidence: {confidence}%",
            (x, y+h+25),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

    if attendance_status and time.time() - status_time < 3:

        cv2.rectangle(
            frame,
            (10, 10),
            (620, 70),
            (0, 170, 0),
            -1
        )

        cv2.putText(
            frame,
            attendance_status,
            (20, 50),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2
        )

    cv2.imshow(
        "SmartAttend AI - Face Recognition",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()