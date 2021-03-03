class Gpa():
    """计算绩点"""
    def __init__(self, grades, year):
        """初始化参数"""
        self.grades = grades
        self.year = year

    def count_gpa(self):
        # 计算学年绩点1(除去公共选修课)
        b = 0
        d = 0
        for grade in self.grades:
            if grade['学年'] == self.year and grade['课程性质'] != '公共选修课':
                a = float(grade['学分']) * float(grade['绩点'])
                b = b + a

                c = float(grade['学分'])
                d = c + d
            else:
                continue
        gpa_0 = str(b / d)

        # 计算学年绩点2(除去所有选修课)
        k = 0
        n = 0
        for grade in self.grades:
            if grade['学年'] == self.year and '选修课' not in grade['课程性质']:
                j = float(grade['学分']) * float(grade['绩点'])
                k = j + k

                m = float(grade['学分'])
                n = m + n
            else:
                continue

        gpa_1 = str(k / n)

        # 计算学位课绩点
        f = 0
        h = 0
        for grade in self.grades:
            if grade['学位课'] == '是':
                e = float(grade['学分']) * float(grade['绩点'])
                f = e + f

                g = float(grade['学分'])
                h = g + h
            else:
                continue

        gpa_2 = str(f / h)

        return gpa_0, gpa_1, gpa_2
