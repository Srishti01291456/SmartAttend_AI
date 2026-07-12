import cv2
import os
import numpy as np
from PIL import Image


dataset_path = "dataset/students"


recognizer = cv2.face.LBPHFaceRecognizer_create()


detector = cv2.CascadeClassifier(
    "models/haarcascade_frontalface_default.xml"
)



def get_images_and_labels(path):

    image_paths=[]


    for root, dirs, files in os.walk(path):

        for file in files:

            if file.endswith(".jpg"):

                image_paths.append(
                    os.path.join(root,file)
                )


    face_samples=[]
    ids=[]


    for image_path in image_paths:


        img = Image.open(
            image_path
        ).convert('L')


        img_numpy=np.array(
            img,
            'uint8'
        )


        folder_name = os.path.basename(
            os.path.dirname(image_path)
        )

        student_id = int(
            folder_name.split("_")[0]
        )


        faces=detector.detectMultiScale(
            img_numpy
        )


        for(x,y,w,h) in faces:


            face_samples.append(
                img_numpy[y:y+h,x:x+w]
            )


            ids.append(
                student_id
            )


    return face_samples,ids




print("Training started...")


faces,ids=get_images_and_labels(
    dataset_path
)


print(
    "Images found:",
    len(faces)
)



recognizer.train(
    faces,
    np.array(ids)
)



os.makedirs("trainer", exist_ok=True)

recognizer.write(
    "trainer/trainer.yml"
)



print("✅ Training Completed")
print("✅ Model saved successfully")