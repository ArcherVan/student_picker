import tkinter as tk
from tkinter import filedialog, messagebox

from core.picker import Picker
from models.student import Student
from storage import loader


class StudentPickerApp:

    def __init__(self):
        # 创建主窗口
        self.window = tk.Tk()
        self.window.title("学生随机抽取器")
        self.window.geometry("600x450")
        self.window.resizable(False, False)

        # 当前学生列表
        self.students = []

        # 当前 Picker
        self.picker = None

        # 创建第一个界面
        self.create_start_page()

    # 第一个界面：学生信息设置

    def create_start_page(self):
        # 标题
        self.title_label = tk.Label(
            self.window,
            text="学生随机抽取器",
            font=("微软雅黑", 22)
        )
        self.title_label.pack(pady=30)

        # 学生人数
        count_frame = tk.Frame(self.window)
        count_frame.pack(pady=10)

        count_label = tk.Label(
            count_frame,
            text="学生人数：",
            font=("微软雅黑", 12)
        )
        count_label.pack(side="left")

        self.count_entry = tk.Entry(
            count_frame,
            width=10,
            font=("微软雅黑", 12)
        )
        self.count_entry.pack(side="left")

        # 手动添加按钮
        manual_button = tk.Button(
            self.window,
            text="手动添加学生",
            width=20,
            command=self.manual_input
        )
        manual_button.pack(pady=10)

        # TXT 导入按钮
        import_button = tk.Button(
            self.window,
            text="从 TXT 导入学生",
            width=20,
            command=self.import_from_txt
        )
        import_button.pack(pady=10)

        # 状态提示
        self.status_label = tk.Label(
            self.window,
            text="请输入学生人数",
            font=("微软雅黑", 10)
        )
        self.status_label.pack(pady=20)

    # 获取学生人数

    def get_student_count(self):
        text = self.count_entry.get().strip()

        try:
            count = int(text)
        except ValueError:
            messagebox.showerror(
                "输入错误",
                "学生人数必须是整数。"
            )
            return None

        if count <= 0:
            messagebox.showerror(
                "输入错误",
                "学生人数必须大于 0。"
            )
            return None

        return count

    # 创建学生

    def create_students(self, count):
        students = []

        for i in range(1, count + 1):
            student = Student(i, "")
            students.append(student)

        return students

    # 手动输入学生

    def manual_input(self):
        count = self.get_student_count()

        if count is None:
            return

        self.students = self.create_students(count)

        self.create_name_page()

    # 创建姓名输入界面

    def create_name_page(self):
        self.clear_window()

        title_label = tk.Label(
            self.window,
            text="请输入学生姓名",
            font=("微软雅黑", 20)
        )
        title_label.pack(pady=20)

        self.name_entries = []

        # 创建姓名输入框
        for student in self.students:
            frame = tk.Frame(self.window)
            frame.pack(pady=3)

            label = tk.Label(
                frame,
                text=f"{student.student_id}号：",
                width=8
            )
            label.pack(side="left")

            entry = tk.Entry(
                frame,
                width=25
            )
            entry.pack(side="left")

            self.name_entries.append(entry)

        # 完成按钮
        finish_button = tk.Button(
            self.window,
            text="完成",
            width=15,
            command=self.finish_manual_input
        )
        finish_button.pack(pady=20)

    # 完成手动输入

    def finish_manual_input(self):
        for i, entry in enumerate(self.name_entries):
            name = entry.get().strip()

            if name == "":
                messagebox.showerror(
                    "输入错误",
                    f"{i + 1}号学生姓名不能为空。"
                )
                return

            self.students[i].name = name

        self.start_picker()

    # TXT 导入

    def import_from_txt(self):
        count = self.get_student_count()

        if count is None:
            return

        filename = filedialog.askopenfilename(
            title="选择学生名单",
            filetypes=[
                ("TXT 文件", "*.txt"),
                ("所有文件", "*.*")
            ]
        )

        # 用户取消选择
        if filename == "":
            return

        students = self.create_students(count)

        success, message = loader.import_names(
            students,
            filename
        )

        if not success:
            messagebox.showerror(
                "导入失败",
                message
            )
            return

        self.students = students

        self.start_picker()

    # 开始抽取

    def start_picker(self):
        self.picker = Picker(self.students)

        self.create_draw_page()

    # 抽取界面

    def create_draw_page(self):
        self.clear_window()

        title_label = tk.Label(
            self.window,
            text="学生随机抽取器",
            font=("微软雅黑", 22)
        )
        title_label.pack(pady=30)

        self.result_label = tk.Label(
            self.window,
            text="等待抽取",
            font=("微软雅黑", 28)
        )
        self.result_label.pack(pady=30)

        # 抽取按钮
        draw_button = tk.Button(
            self.window,
            text="抽取学生",
            width=20,
            height=2,
            command=self.draw_student
        )
        draw_button.pack(pady=10)

        # 重新开始
        reset_button = tk.Button(
            self.window,
            text="重新开始",
            width=20,
            command=self.reset_picker
        )
        reset_button.pack(pady=10)

        # 返回设置
        back_button = tk.Button(
            self.window,
            text="重新设置学生",
            width=20,
            command=self.back_to_start
        )
        back_button.pack(pady=10)

        self.count_label = tk.Label(
            self.window,
            text=self.get_count_text()
        )
        self.count_label.pack(pady=10)

    # 抽取学生

    def draw_student(self):
        student = self.picker.pick()

        if student is None:
            messagebox.showinfo(
                "抽取结束",
                "所有学生都已经抽取过了。"
            )
            return

        self.result_label.config(
            text=f"{student.student_id}号 - {student.name}"
        )

        self.count_label.config(
            text=self.get_count_text()
        )

    # 重新开始

    def reset_picker(self):
        self.picker.reset()

        self.result_label.config(
            text="等待抽取"
        )

        self.count_label.config(
            text=self.get_count_text()
        )

    # 返回开始页面

    def back_to_start(self):
        self.picker = None
        self.students = []

        self.clear_window()
        self.create_start_page()

    # 获取抽取数量信息

    def get_count_text(self):
        if self.picker is None:
            return ""

        picked_count = len(self.picker.picked)
        total_count = len(self.students)

        return f"已抽取：{picked_count} / {total_count}"

    # 清空窗口

    def clear_window(self):
        for widget in self.window.winfo_children():
            widget.destroy()

    # 启动程序

    def run(self):
        self.window.mainloop()

