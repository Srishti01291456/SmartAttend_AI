import cv2

print("OpenCV Version:", cv2.__version__)

print("CascadeClassifier:",
      hasattr(cv2, "CascadeClassifier"))

print("Face Module:",
      hasattr(cv2, "face"))