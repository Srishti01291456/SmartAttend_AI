import os
import cv2
import shutil

from database import load_students

# -------------------------------
# Load Student Database
# -------------------------------

students = load_students()

student_id = input("Enter Student ID: ").strip()

if student_id not in students:
    print("Student ID not found. Please register the student first.")
    exit()

student_name = students[student_id]

dataset_path = os.path.join(
    "dataset",
    "students",
    f"{student_id}_{student_name}"
)

# -------------------------------
# Check Existing Images
# -------------------------------

if os.path.exists(dataset_path):

    existing_images = [
        f for f in os.listdir(dataset_path)
        if f.endswith(".jpg")
    ]

    print(f"\nStudent '{student_name}' already has {len(existing_images)} images.")

    print("\nChoose an option:")
    print("1. Overwrite existing images")
    print("2. Add more images")
    print("3. Cancel")

    choice = input("\nEnter choice (1/2/3): ").strip()

    if choice == "1":

        shutil.rmtree(dataset_path)
        os.makedirs(dataset_path)

        count = 0

        print("\nOld images deleted.")

    elif choice == "2":

        count = len(existing_images)

        print(f"\nContinuing from image {count + 1}")

    else:

        print("Operation cancelled.")
        exit()

else:

    os.makedirs(dataset_path)
    count = 0


# -------------------------------
# Load Face Detector
# -------------------------------

face_detector = cv2.CascadeClassifier(
    "models/haarcascade_frontalface_default.xml"
)

if face_detector.empty():
    print("Could not load Haar Cascade.")
    exit()


# -------------------------------
# Start Camera
# -------------------------------

camera = cv2.VideoCapture(0)

if not camera.isOpened():
    print("Cannot access webcam.")
    exit()


MAX_IMAGES = count + 100

print(f"\nCapturing images for {student_name}")
print("Press Q to stop early.\n")


while True:

    ret, frame = camera.read()

    if not ret:
        break

    gray = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2GRAY
    )

    faces = face_detector.detectMultiScale(
        gray,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(100, 100)
    )

    for (x, y, w, h) in faces:

        face = gray[y:y+h, x:x+w]

        face = cv2.resize(
            face,
            (200, 200)
        )

        count += 1

        image_path = os.path.join(
            dataset_path,
            f"{count}.jpg"
        )

        cv2.imwrite(
            image_path,
            face
        )

        cv2.rectangle(
            frame,
            (x, y),
            (x+w, y+h),
            (0, 255, 0),
            2
        )

        cv2.putText(
            frame,
            f"Capturing Images: {count}/{MAX_IMAGES}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        break

    cv2.imshow(
        "SmartAttend AI - Face Capture",
        frame
    )

    key = cv2.waitKey(80) & 0xFF

    if key == ord("q"):
        break

    if count >= MAX_IMAGES:
        break


camera.release()
cv2.destroyAllWindows()

print("\nCapture Complete.")
print(f"Total images available for {student_name}: {count}")
print("\nNow run:")
print("python src/train_model.py")