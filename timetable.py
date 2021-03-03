import requests
import re
from bs4 import BeautifulSoup


class Get_timetable():
    '''获取课程表'''
    def __init__(self, url_head, xh, xm):
        self.url_head = url_head
        self.xh = xh
        self.xm = xm

    def timetable_website(self):
        """跳转到课程表页面"""
        url_N121603 = self.url_head + 'xskbcx.aspx?xh=' + self.xh + '&xm=' + self.xm + '&gnmkdm=N121603'
        # 跳转课程表页面请求头，不全可能会导致跳转失败
        headers_N121603 = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding':
            'gzip, deflate',
            'Accept-Language':
            'zh-CN,zh;q=0.9',
            'Connection':
            'keep-alive',
            'DNT':
            '1',
            'Host':
            'jxw.sylu.edu.cn',
            'Origin': 'http://jxw.sylu.edu.cn',
            'Referer':
            self.url_head + 'xs_main.aspx?xh=' + self.xh,
            'Upgrade-Insecure-Requests':
            '1',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
        }

        resp_N121603 = requests.post(url_N121603, headers=headers_N121603)
        self.resp_N121603 = resp_N121603.text
        print(self.resp_N121603)

    def get_course(self):
        """提取相关信息"""
        bs = BeautifulSoup(self.resp_N121603, 'lxml')
        # print(bs)

        # 姓名
        name = bs.find(id='Label6')
        name = name.string[3:]

        # 学院
        college = bs.find(id='Label7')
        college = college.string[3:]

        # 专业
        major = bs.find(id='Label8')
        major = major.string[3:]

        # 课表
        t_list = bs.find_all(rowspan='2')

        # 正则表达式提取信息，创建课程表字典，并嵌套到列表中
        courses = []
        i = 0

        for item in t_list:
            item = str(item)
            matchobj = re.findall('(>.*?<)', item)
            current_course = {}
            current_course['Lesson'] = (matchobj[0])[1:-1]
            current_course['Time'] = (matchobj[1])[1:-1]
            current_course['Teacher'] = (matchobj[2])[1:-1]
            current_course['Position'] = (matchobj[3])[1:-1]

            exec('course_' + str(i) + ' = current_course')
            exec('courses.append(' + 'course_' + str(i) + ')')
            i = i + 1

        # 返回一个包含姓名，学院，专业，课表的列表
        info = {
            'name': name,
            'college': college,
            'major': major,
            'courses': courses
        }
        return info
