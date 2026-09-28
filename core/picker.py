from models.student import Student
import random
class Picker:
    def __init__(self,students):
        self.students = students
        self.picked = set()

    def pick(self):
        if len(self.picked) == len(self.students):
            return None
        stu = random.choice(self.students)
        while stu.student_id in self.picked:
            stu = random.choice(self.students)
        self.picked.add(stu.student_id)
        return stu

    def reset(self):
        self.picked.clear()

