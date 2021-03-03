import requests
from bs4 import BeautifulSoup
import sys


class Login:
    """模拟登录教务系统"""

    def __init__(self, xh, pw, url_head):
        """初始化参数"""
        self.xh = str(xh)
        self.pw = str(pw)
        self.url_head = url_head

    def login_website(self):
        """模拟登录"""
        url_login = self.url_head + 'default2.aspx'  # 提交表单地址
        url_0 = self.url_head + 'xs_main.aspx?xh=' + self.xh  # 登陆后默认显示地址

        # 设置请求头
        headers_0 = {
            'User-agent':
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
        }

        # 构造Session
        session = requests.session()

        # 需要提交的表单
        data = {
            '__VIEWSTATE': 'dDwxODI0OTM5NjI1Ozs+ErNwwEBfve9YGjMA8xEN6zdawEw=',
            'TextBox1': self.xh,
            'TextBox2': self.pw,
            'RadioButtonList1': '学生',
            'Button1': '',
            'lbLanguage': ''
        }

        try:
            # 在Session中发送登录请求，此后这个session里就存储了cookie
            # 查看session
            # print(session.cookies.get_dict())
            session.post(url_login, headers=headers_0, data=data)

            # 发送访问请求
            resp = session.get(url_0)
            bs_0 = BeautifulSoup(resp.text, 'lxml')
            xm = bs_0.find(id='xhxm')
            xm = xm.string[12:-2]
            # print(xm)
            return xm

        except:
            print('\n登录失败，请检查账号密码是否错误，或检查网络设置\n')
            input()
            sys.exit(0)
