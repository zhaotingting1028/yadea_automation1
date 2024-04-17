import unittest
import HTMLTestReportCN
import time
from Core.feishu_send import *
from Core.send_email import *


class Run_TestCase():

    def run(self,dir):

        tmp = time.strftime("%Y%d%m_%H%M%S", time.localtime(time.time()))
        # # 执行发送飞书文本消息
        # content = tmp + ".html"
        # FeishuTalk().sendTextmessage(content)

        # 生成自动化报告
        with open(f"./reports/{tmp}.html", 'wb') as file:
            runner = HTMLTestReportCN.HTMLTestRunner(stream=file, title="接口自动化测试报告")
            suite = unittest.defaultTestLoader.discover(start_dir= dir, pattern="*.py")
            runner.run(suite)
        # 执行发送邮件消息
        # send_mail_report("DFB of Api Test Report!!!")

if __name__ == '__main__':

    Run_TestCase().run('./TestCase/TestTickets/')
