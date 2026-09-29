def load_names_from_file(filename):
    names = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip() == "":
                    continue
                names.append(line.strip())
    except FileNotFoundError:
        return None
    return names

def import_names(students, filename):
    names = load_names_from_file(filename)
    if names is None:
        return False,"文件不存在"
    if len(names) != len(students):
        return False,"文件人数和学生人数不匹配"
    assign_names(students, names)
    return True,"导入成功"


def assign_names(students, names):
    if len(students) != len(names):
        print("数据和人数不匹配,请重新导入数据")
        return False
    for i in range(len(students)):
        students[i].name = names[i]
    return students


