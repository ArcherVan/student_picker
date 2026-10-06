import json
from models.student import Student
def save_students(students):
    with open("students.json", "w", encoding="utf-8") as f:
        json.dump(students_to_dict(students), f, ensure_ascii=False, indent=4)

def load_students():
    try:
        with open("students.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            return dict_to_students(data)
    except FileNotFoundError:
        return []
    
def student_to_dict(student):
    result = {}
    result['student_id'] = student.student_id
    result['name'] = student.name
    return result

def students_to_dict(students):
    result = []
    for stu in students:
        result.append(student_to_dict(stu))
    return result

def dict_to_student(data):
    student = Student(
        data["student_id"],
        data["name"]
    )
    return student

def dict_to_students(data):
    students = []
    for dt in data:
        students.append(dict_to_student(dt))
    return students


