import csv
import os


BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)


DATABASE_FILE = os.path.join(
    BASE_DIR,
    "database",
    "students.csv"
)



# ---------------------------------
# Check Existing Student
# ---------------------------------
def student_exists(student_id):

    if not os.path.exists(DATABASE_FILE):
        return False


    with open(
        DATABASE_FILE,
        "r"
    ) as file:

        reader = csv.DictReader(file)


        for row in reader:

            existing_id = row.get("ID") or row.get("id")

            if existing_id == str(student_id):
                return True


    return False




# ---------------------------------
# Add Student
# ---------------------------------

def add_student(student_id, student_name):


    os.makedirs(
        os.path.dirname(DATABASE_FILE),
        exist_ok=True
    )


    # Check duplicate

    if student_exists(student_id):

        print(
            "⚠️ Student already registered!"
        )

        return False



    file_exists = os.path.exists(
        DATABASE_FILE
    )


    with open(
        DATABASE_FILE,
        "a",
        newline=""
    ) as file:


        writer = csv.writer(file)


        if not file_exists:

            writer.writerow(
                [
                    "ID",
                    "Name"
                ]
            )


        writer.writerow(
            [
                student_id,
                student_name
            ]
        )


    print(
        "✅ Student registered successfully"
    )


    return True




# ---------------------------------
# Load Students
# ---------------------------------

def load_students():

    students = {}


    if not os.path.exists(DATABASE_FILE):
        return students


    with open(
        DATABASE_FILE,
        "r"
    ) as file:

        reader = csv.DictReader(file)


        for row in reader:

            student_id = row.get("ID") or row.get("id")
            name = row.get("Name") or row.get("name")

            students[student_id] = name


    return students