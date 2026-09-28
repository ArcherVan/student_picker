class Student:
    def __init__(self,student_id, name):
        self.student_id = student_id
        self.name = name

    def show_info(self) :
            print("%d号 - %s" %(self.student_id,self.name))

