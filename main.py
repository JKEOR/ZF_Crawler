import requests
from login import Login
from timetable import Get_timetable
from lesson import LessonPlan
from score import Score
from gpa import Gpa


def main():
    """爬取正方教务系统（以沈阳理工大学教务系统为例，其余学校可能不适用）"""
    url = 'http://jxw.sylu.edu.cn/'  # 登录网址，网址最后务必加上'/'，否则无法识别
    xh = str(input("请输入学号："))  # 登录账号
    pw = str(input("请输入密码："))  # 登录密码

    # 登录教务系统
    r = requests.get(url)
    url_head = str(r.url)[0:50]  # 网站会自动跳转，获取网址前缀
    login = Login(xh, pw, url_head)
    xm = login.login_website()
    print("\n欢迎您，%s" % xm)

    # 获取教学计划学位课信息
    lesson = LessonPlan(url_head, xh, xm)
    lesson_list = lesson.get_lesson()

    # 获取考试成绩
    score = Score(url_head, xh, xm, lesson_list)
    score.get_page()
    grades = score.get_data()

    print("输入数字1/2/3/4选择对应功能，输入q退出程序")
    print("1-成绩查询\t2-绩点计算\t3-课表查询\t4-一键抢课\tq-退出程序")
    ch = ''
    while ch != 'q':
        ch = input("请输入\t")

        if ch == '1':
            print("1-成绩查询")
            print('\n', xm)
            for grade in grades:
                print(grade['学年'], grade['学期'], grade['课程名称'], '---',
                      grade['成绩'])

        elif ch == '2':
            print("2-绩点计算")
            # 获取有成绩的年份
            years = []
            for grade in grades:
                years.append(grade['学年'])
            years = list(set(years))
            # 计算绩点
            print('\n', xm)
            for year in years:
                get_gpa = Gpa(grades, year)
                gpa_list = get_gpa.count_gpa()
                print(year + "学年绩点1(除去公共选修课)：" + gpa_list[0])
                print(year + "学年绩点2(除去所有选修课)：" + gpa_list[1], '\n')
            print("学位课绩点：" + gpa_list[2])

        elif ch == '3':
            print("3-课表查询")
            tt = Get_timetable(url_head, xh, xm)
            tt.timetable_website()
            info = tt.get_course()
            courses = info['courses']
            # 打印课程信息
            print('姓名: ', info['name'])
            print('学院: ', info['college'])
            print('专业: ', info['major'])
            for course in courses:
                print(course)

        elif ch == '4':
            print("4-一键抢课")
            print("待写")
            pass

        elif ch == 'q':
            break

        else:
            print("输入无效，请重新输入")
            continue


if __name__ == "__main__":
    main()
