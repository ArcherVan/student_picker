class Student:
    def __init__(self,student_id, name):
        self.student_id = student_id
        self.name = name
        
    def __str__(self):
        return f"{self.student_id}号 - {self.name}"

