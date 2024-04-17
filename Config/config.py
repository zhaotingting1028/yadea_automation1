# -*- coding:utf-8 -*-
import os

#azure otests数据库
td_report = dict(host='192.168.10.109', user='root', passwd='Hx12345678', port=3306, db='test_ztt',
                 charset='gbk')
# 日志配置
import logging

logpath = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'log')
# logging.basicConfig(level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%y-%m-%d %H:%M',
                    filename=os.path.join(logpath, 'log.txt'),
                    filemode='a')


#日志执行人配置
test_name = 'ZTT'

# 项目根路径配置
basedir = os.path.split(os.path.split(os.path.abspath(__file__))[0])[0]

# 邮件配置
sender = '827336571@qq.com'  # 发送方1
receiver = '827336571@qq.com' # 接收方
emailusername = '827336571@qq.com'  # 登陆邮箱的用户名
emailpassword = 'kjstdnueocpibcch'  # 登陆邮箱的授权码kjstdnueocpibcch,授权码_84ca
server = 'smtp.qq.com' #发件服务地址exmail.
subject = '接口自动化报告'  # 邮件主题
content = '接口自动化报告在附件请注意查收'  # 邮件正文
data_zip = basedir+"\\reports\\DFBAPITestReport.zip" # 获取邮件目录

# 车架号list配置
vim_data = ["LR4DE1DA1N1178972","779422380006174","L5XDE1Z43P6311800","L5XDE1ZN3P6023607",
       "779422351388614","LR4NE0609L1365151","779422112086401","LR4NE05AXP1224511",
       "LR4NE0FH3N3025667","779422310299104","L5XDE1ZN7P6050731","779422280164896",
       "HJ8DEHNF1P8010868","779422320644919","779422320234212","779422310004226",
       "779422333997782","779422253064799","779422310095294","779421860549258",
       "779421860549258","779421860549258","779422323134133","779422310587218",
       "779422322607022","779422310128503","L5XDE1Z15N6273506","LR4DE15B0P2023012",
        "LR4DE1DA8P1107299","779422251248305","779422320891037","779422323122456"]

