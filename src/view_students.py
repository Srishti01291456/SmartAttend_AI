from database import load_students



students = load_students()


print("\nRegistered Students")
print("--------------------")


if len(students) == 0:

    print("No students registered")


else:

    for student_id, name in students.items():

        print(
            f"ID: {student_id} | Name: {name}"
        )