import requests
from bs4 import BeautifulSoup


class Score():
    """获取成绩"""
    def __init__(self, url_head, xh, xm, lesson_list):
        """初始化参数"""
        self.url_head = url_head
        self.xh = xh
        self.xm = xm
        self.lesson_list = lesson_list

    def get_page(self):
        # 获取成绩网址
        url_N121605 = self.url_head + 'xscjcx.aspx?xh=' + self.xh + '&xm=' + self.xm + '&gnmkdm=N121605'

        # 获取POST所需的_VIEWSTATE数据
        headers_0 = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
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
            'Referer':
            self.url_head + 'xs_main.aspx?xh=' + self.xh,
            'Upgrade-Insecure-Requests':
            '1',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        url_N121605 = self.url_head + 'xscjcx.aspx?xh=' + self.xh + '&xm=' + self.xm + '&gnmkdm=N121605'
        resp_N121605 = requests.get(url_N121605, headers=headers_0)
        bs_0 = BeautifulSoup(resp_N121605.text, 'lxml')
        viewstate = bs_0.find(type="hidden")
        viewstate = viewstate.next_sibling.next_sibling.next_sibling.next_sibling
        viewstate = str(viewstate['value'])

        # 跳转成绩页面请求头，不全可能会导致跳转失败
        headers_1 = {
            'Accept':
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding':
            'gzip, deflate',
            'Accept-Language':
            'zh-CN,zh;q=0.9',
            'Cache-Control':
            'max-age=0',
            'Connection':
            'keep-alive',
            'Content-Length':
            '4264',
            'Content-Type':
            'application/x-www-form-urlencoded',
            'DNT':
            '1',
            'Host':
            'jxw.sylu.edu.cn',
            'Origin':
            'http://jxw.sylu.edu.cn',
            'Referer':
            self.url_head + 'xs_main.aspx?xh=' + self.xh,
            'Upgrade-Insecure-Requests':
            '1',
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }
        # 成绩页面POST数据
        data_1 = {
            '__EVENTTARGET': '',
            '__EVENTARGUMENT': '',
            '__VIEWSTATE': viewstate,
            'hidLanguage': '',
            'ddlXN': '',
            'ddlXQ': '',
            'ddl_kcxz': '',
            'btn_zcj': '历年成绩'
        }

        # 请求登录
        resp_data = requests.post(url_N121605, headers=headers_1, data=data_1)
        self.resp_data = resp_data.text

    def get_data(self):
        # 获取数据
        bs = BeautifulSoup(self.resp_data, 'lxml')

        # 成绩
        result = bs.find(text='学年')
        grades = []
        for tt in result.parent.parent.parent.next_siblings:
            t_list = []

            # 筛选包含成绩的Tag
            if str(type(tt)) == "<class 'bs4.element.Tag'>":
                for t in tt.children:
                    t_list.append(t.string)

                current_grade = {}
                current_grade['学年'] = (t_list[1])
                current_grade['学期'] = (t_list[2])
                current_grade['课程代码'] = (t_list[3])
                current_grade['课程名称'] = (t_list[4])
                current_grade['课程性质'] = (t_list[5])
                current_grade['学分'] = (t_list[7])
                current_grade['绩点'] = (t_list[8])
                current_grade['平时成绩'] = (t_list[9])
                current_grade['期末成绩'] = (t_list[11])
                current_grade["成绩"] = (t_list[13])
                current_grade['补考成绩'] = (t_list[15])
                current_grade['重修标记'] = (t_list[20])
                current_grade['学位课'] = None
                grades.append(current_grade)
            else:
                continue

        # 创建成绩列表
        for grade in grades:
            for key, value in self.lesson_list.items():
                if grade['课程代码'] == key:
                    grade['学位课'] = value
                else:
                    continue

            for g in grades:
                if grade['课程代码'] == g['课程代码']:
                    grade['绩点'] = g['绩点']
                    grade['期末成绩'] = g['期末成绩']
                    grade['成绩'] = g['成绩']
                    grade['重修标记'] = g['重修标记']
                    if g['重修标记'] == '重修':
                        grades.remove(g)

        return grades
