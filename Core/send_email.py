# -*- coding: utf-8 -*-
import mimetypes
from email import encoders
from email.mime.base import MIMEBase
import smtplib
import base64
from email.mime.text import MIMEText#发送纯文本信息
from email.mime.multipart import MIMEMultipart#混合信息
from Config import config
import sys
sys.path.append(config.basedir+'')
import os
import zipfile
import time

def zip_report(input_path,output_path,output_name):
    """将测试报告生成压缩文件,By Wendy"""
    f = zipfile.ZipFile(output_path+'/'+output_name,'w',zipfile.ZIP_DEFLATED)
    files = os.listdir(input_path)
    for file in files:
        if (os.path.splitext(file)[1] == ".html"):
            f.write(input_path + '/' + file)
    f.close()
    return output_path+r"/"+output_name

def send_mail_report(title):
    """将测试报告发送到邮件"""

    """获取测试报告邮件服务器、发件人、收件人等信息"""
    sender = config.sender  # 测试报告邮件发件人邮件地址
    receiver = config.receiver # 测试报告邮件收件人
    server = config.server # 测试报告邮箱服务器smtp服务器
    username = config.emailusername  #测试报告邮件发件人邮箱账户
    password = config.emailpassword # 测试报告邮件发件人邮箱密码

    """获取最新测试报告"""
    reportPath=config.basedir+"/reports/"
    newReport = ""
    for root, subdirs, files in os.walk(reportPath):
        for file in files:
            if os.path.splitext(file)[1] == ".html":  # 判断该目录下的文件扩展名是否为html
                newReport=file

    #改变当前的相对路径由 testSuite变更为report,然后压缩report下面的测试报告Report.html文件
    os.chdir(reportPath)
    cwd = os.getcwd()
    print("cwd is:"+cwd)
    zip_report(r"./", './', 'DFBAPITestReport.zip') # 将Report.html文件压缩成.zip文件，存放路径为./reports

    """生成邮件的内容"""
    msg=MIMEMultipart()
    msg["subject"] = title
    msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
    with open(os.path.join(reportPath, newReport), 'rb') as f:
        mailbody = f.read()
    html = MIMEText(mailbody, _subtype='html', _charset='utf-8')
    msg.attach(html)

    # """将测试报告压缩文件添加到邮件附件"""
    data = open(config.data_zip, 'rb')
    ctype, encoding = mimetypes.guess_type(config.data_zip)
    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'
    maintype, subtype = ctype.split('/', 1)
    file_msg = MIMEBase(maintype, subtype)
    file_msg.set_payload(data.read())
    data.close()
    encoders.encode_base64(file_msg)  # 把附件编码
    # 修改附件名称
    file_msg.add_header('Content-Disposition', 'attachment', filename="DFBAPITestReport.zip")
    msg.attach(file_msg)

    """发送邮件"""
    msg['from'] = sender
    try:
        # smtp = smtplib.SMTP_SSL(server, 465)
        # smtp.set_debuglevel(1)
        smtp = smtplib.SMTP(timeout=30)
        smtp.connect(server, 25)
        smtp.login(username, password)
        smtp.sendmail(sender, receiver.split(','), msg.as_string())
        smtp.close()
        print("邮件发送成功")
    except Exception:
        print("Error :无法发送邮件")
        raise

