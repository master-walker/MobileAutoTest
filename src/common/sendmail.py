#!/usr/bin/python
#coding=cp936
'''
Created on 2011-8-16
@author: jxh
Description:

'''
import smtplib,os  
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
from email.MIMEBase import MIMEBase
from email.Utils import COMMASPACE, formatdate 
from email import encoders

#server['host'], server['user'], server['passwd']
def send_mail(server, fro, to, subject, text, files=[]): 
    assert type(server) == dict 
    assert type(to) == list 
    assert type(files) == list 
 
    msg = MIMEMultipart() 
    msg['From'] = fro
    msg['Subject'] = subject 
    msg['To'] = COMMASPACE.join(to)
    msg['Date'] = formatdate(localtime=True) 
    msg.attach(MIMEText(text,'html','GBK')) 
    for file in files: 
        part = MIMEBase('application', 'octet-stream') #'octet-stream': binary data 
        part.set_payload(open(file,'rb').read()) 
        encoders.encode_base64(part) 
        part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(file)) 
        msg.attach(part) 
    #smtp = smtplib.SMTP(server['host']) 
    smtp = smtplib.SMTP_SSL(server['host'],465)
    #smtp.set_debuglevel(1)
    smtp.login(server['user'], server['passwd']) 
    smtp.sendmail(fro, to, msg.as_string()) 
    smtp.close()

#send_mail({'host':'smtpcom.263xmail.com','user':'jiangxiaohu@1218.com.cn','passwd':'Rzx123'},\
#           'jiangxiaohu@1218.com.cn', ['mail_spam@126.com'], '邮件程序测试邮件', '邮件内容',['C:\\Regx.xml'])
#send_mail({'host':'smtp.126.com','user':'mail_spam','passwd':'99819981'},\
#           'mail_spam@126.com', ['mail_spam@126.com'], '邮件程序测试邮件', '邮件内容',['C:\\Regx.xml'])