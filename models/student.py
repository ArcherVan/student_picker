from config.settings import MIN_STUDENT_ID, MAX_STUDENT_ID
class Student:
    def __init__(self,student_id, name):
        self.student_id = student_id
        self.check_student_id()
        self.name = name
        
    def __str__(self):
        return f"{self.student_id}号 - {self.name}"

    def check_student_id(self):
        if MIN_STUDENT_ID <= self.student_id <= MAX_STUDENT_ID:
            return 
        raise ValueError(f"学号必须在{MIN_STUDENT_ID} 到{MAX_STUDENT_ID}之间，当前值:{self.student_id}")


