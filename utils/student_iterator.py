def student_generator(students):
    for student in students:
        yield student

def passed_student_generator(students):
    for student in students:
        if student.student_id % 2 == 0:
            yield student