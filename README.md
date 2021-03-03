# ZF_Crawler
用python写的爬取正方教务管理系统。
目前实现的功能：1.成绩查询  2.计算绩点  3.课表查询
抢课功能待完成

使用方法：直接运行main.py，按提示输入学号密码即可，仅可用于沈阳理工大学，其余学校需要在main.py中更改教务网址 。
如若不能使用或存在bug，欢迎提交issue。

main.py -- 主程序  
login.py -- 模拟登录  
lesson.py -- 爬取教学计划  
score.py -- 查询成绩  
gpa.py -- 计算绩点  
timetable.py -- 查询课表  
