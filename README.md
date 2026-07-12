# SmartAttend AI

An AI-powered Face Recognition Attendance System built with Python, OpenCV, Streamlit, and OpenPyXL.

## Features

- Face Detection
- Face Recognition using LBPH
- Automatic Attendance Marking
- Excel Attendance Report
- Streamlit Dashboard
- Student Registration
- Add New Students and Retrain Model

## Technologies

- Python
- OpenCV
- OpenCV-Contrib
- Streamlit
- Pandas
- OpenPyXL
- Pillow

## Project Structure

```
SmartAttend_AI/
│
├── attendance/
├── database/
├── dataset/
├── models/
├── src/
├── trainer/
└── dashboard.py
```

## Installation

```bash
git clone https://github.com/<your-username>/SmartAttend_AI.git
cd SmartAttend_AI

python -m venv venv

# Windows
venv\Scripts\activate

pip install -r requirements.txt
```

## Run the Project

Register a student:

```bash
python src/register_student.py
```

Capture images:

```bash
python src/face_detector.py
```

Train the model:

```bash
python src/train_model.py
```

Run recognition:

```bash
python src/face_recognition.py
```

Run dashboard:

```bash
streamlit run dashboard.py
```

## Author

Srishti