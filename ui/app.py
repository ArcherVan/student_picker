import tkinter as tk
from tkinter import filedialog, messagebox
from core.picker import Picker
from models.student import Student
from storage import loader, repository


class StudentPickerApp:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("学生随机抽取器")
        self.window.geometry("560x430")
        self.window.resizable(False, False)

        # 启动时加载已经保存的学生
        self.students = repository.load_students()
        self.picker = None

        self.create_start_page()

    def clear_window(self):
        """清空当前窗口中的所有控件"""
        for widget in self.window.winfo_children():
            widget.destroy()

    def create_start_page(self):
        """创建开始页面"""
        self.clear_window()

        title_font = ("Microsoft YaHei UI", 22, "bold")
        label_font = ("Microsoft YaHei UI", 10)
        button_font = ("Microsoft YaHei UI", 10)

        # 页面主容器
        main_frame = tk.Frame(self.window)
        main_frame.pack(expand=True)

        # 标题
        title = tk.Label(
            main_frame,
            text="学生随机抽取器",
            font=title_font
        )
        title.pack(pady=(0, 22))

        # 学生人数输入
        count_frame = tk.Frame(main_frame)
        count_frame.pack(pady=(0, 15))

        count_label = tk.Label(
            count_frame,
            text="学生人数",
            font=label_font
        )
        count_label.pack()

        self.count_entry = tk.Entry(
            count_frame,
            width=20,
            font=("Microsoft YaHei UI", 10),
            justify="center"
        )
        self.count_entry.pack(pady=(6, 0))

        # 统一按钮配置
        button_config = {
            "font": button_font,
            "width": 18,
            "height": 1
        }

        # 手动输入
        manual_button = tk.Button(
            main_frame,
            text="手动输入学生",
            command=self.manual_input,
            **button_config
        )
        manual_button.pack(pady=4)

        # TXT 导入
        import_button = tk.Button(
            main_frame,
            text="从 TXT 文件导入",
            command=self.import_from_txt,
            **button_config
        )
        import_button.pack(pady=4)

        # 已保存学生
        if self.students:
            saved_button = tk.Button(
                main_frame,
                text=f"使用已保存学生（{len(self.students)}人）",
                command=self.start_picker,
                **button_config
            )
            saved_button.pack(pady=4)

        # 状态提示
        self.status_label = tk.Label(
            main_frame,
            text="",
            font=("Microsoft YaHei UI", 9)
        )
        self.status_label.pack(pady=(10, 0))

    def get_student_count(self):
        """获取并检查学生人数"""
        try:
            count = int(self.count_entry.get())

            if count <= 0:
                self.status_label.config(
                    text="学生人数必须大于0"
                )
                return None

            return count

        except ValueError:
            self.status_label.config(
                text="请输入正确的整数"
            )
            return None

    def create_students(self, count):
        """根据人数创建学生对象"""
        students = []

        for i in range(1, count + 1):
            students.append(Student(i, ""))

        return students

    def manual_input(self):
        """进入手动输入学生姓名页面"""
        count = self.get_student_count()

        if count is None:
            return

        self.students = self.create_students(count)

        self.clear_window()

        title = tk.Label(
            self.window,
            text="请输入学生姓名",
            font=("Microsoft YaHei UI", 18, "bold")
        )
        title.pack(pady=20)

        self.name_entries = []

        for student in self.students:
            frame = tk.Frame(self.window)
            frame.pack(pady=3)

            label = tk.Label(
                frame,
                text=f"{student.student_id}号：",
                width=8,
                font=("Microsoft YaHei UI", 10)
            )
            label.pack(side=tk.LEFT)

            entry = tk.Entry(
                frame,
                width=30,
                font=("Microsoft YaHei UI", 10)
            )
            entry.pack(side=tk.LEFT)

            self.name_entries.append(entry)

        finish_button = tk.Button(
            self.window,
            text="完成",
            width=15,
            font=("Microsoft YaHei UI", 10),
            command=self.finish_manual_input
        )
        finish_button.pack(pady=20)

    def finish_manual_input(self):
        """完成手动输入"""
        for i, entry in enumerate(self.name_entries):
            name = entry.get().strip()

            if name == "":
                messagebox.showwarning(
                    "提示",
                    f"{i + 1}号学生姓名不能为空"
                )
                return

            self.students[i].name = name

        # 保存学生数据
        repository.save_students(self.students)

        self.start_picker()

    def import_from_txt(self):
        """从TXT文件导入学生姓名"""
        count = self.get_student_count()

        if count is None:
            return

        filename = filedialog.askopenfilename(
            title="选择学生名单",
            filetypes=[
                ("TXT文件", "*.txt"),
                ("所有文件", "*.*")
            ]
        )

        if not filename:
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

        # 保存导入的学生数据
        repository.save_students(self.students)

        messagebox.showinfo(
            "导入成功",
            message
        )

        self.start_picker()

    def start_picker(self):
        """开始抽取"""
        if not self.students:
            messagebox.showwarning(
                "提示",
                "当前没有学生数据"
            )
            return

        self.picker = Picker(self.students)

        self.create_draw_page()

    def create_draw_page(self):
        """创建抽取页面"""
        self.clear_window()

        # 抽取页面主容器
        main_frame = tk.Frame(self.window)
        main_frame.pack(expand=True)

        # 标题
        title = tk.Label(
            main_frame,
            text="学生随机抽取",
            font=("Microsoft YaHei UI", 20, "bold")
        )
        title.pack(pady=(0, 18))

        # 当前抽取结果
        self.result_label = tk.Label(
            main_frame,
            text="准备抽取",
            font=("Microsoft YaHei UI", 22, "bold")
        )
        self.result_label.pack(pady=(0, 12))

        # 抽取进度
        self.count_label = tk.Label(
            main_frame,
            text=self.get_count_text(),
            font=("Microsoft YaHei UI", 10)
        )
        self.count_label.pack(pady=(0, 18))

        # 抽取按钮
        draw_button = tk.Button(
            main_frame,
            text="抽取学生",
            width=18,
            height=1,
            font=("Microsoft YaHei UI", 10),
            command=self.draw_student
        )
        draw_button.pack(pady=5)

        # 重新开始按钮
        reset_button = tk.Button(
            main_frame,
            text="重新开始抽取",
            width=18,
            height=1,
            font=("Microsoft YaHei UI", 10),
            command=self.reset_picker
        )
        reset_button.pack(pady=5)

        # 返回设置按钮
        back_button = tk.Button(
            main_frame,
            text="返回设置",
            width=18,
            height=1,
            font=("Microsoft YaHei UI", 10),
            command=self.back_to_start
        )
        back_button.pack(pady=5)

    def draw_student(self):
        """抽取一个学生"""
        student = self.picker.pick()

        if student is None:
            self.result_label.config(
                text="所有学生都已经抽取过了"
            )
            return

        print(student)

        self.result_label.config(
            text=str(student)
        )

        self.count_label.config(
            text=self.get_count_text()
        )

    def reset_picker(self):
        """重新开始抽取"""
        if self.picker is None:
            return

        self.picker.reset()

        self.result_label.config(
            text="准备抽取"
        )

        self.count_label.config(
            text=self.get_count_text()
        )

    def get_count_text(self):
        """获取抽取进度"""
        if self.picker is None:
            return ""

        picked_count = len(self.picker.picked)
        total_count = len(self.students)

        return f"已抽取：{picked_count} / {total_count}"

    def back_to_start(self):
        """返回开始页面"""
        self.picker = None

        # 重新读取保存的数据
        self.students = repository.load_students()

        self.create_start_page()

    def run(self):
        """运行程序"""
        self.window.mainloop()


if __name__ == "__main__":
    app = StudentPickerApp()
    app.run()