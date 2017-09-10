#!/usr/bin/python
#coding=gb2312
'''
Created on 2011-10-26
@author: jxh
Description:

'''
import poplib,time,base64,re
def get_mail_info(server,user,password,topmailnum=0):
    mails = []
    # 创建一个pop3对象，这个时候实际上已经连接上服务器了
    pop3 = poplib.POP3(server)
    # 设置调试模式，可以看到与服务器的交互信息
    #pp.set_debuglevel(1)
    # 向服务器发送用户名
    pop3.user(user)
    # 向服务器发送密码
    pop3.pass_(password)
    # 获取服务器上信件信息，返回是一个两个元素的列表，第一项是一共有多少封邮件，第二项是共有多少字节
    emailMsgNum,emailMsgSize = pop3.stat()
    #print emailMsgNum
    if topmailnum==0:
        topmailnum = emailMsgNum

    p = re.compile("=\?.+\?.\?")    
    for i in range(emailMsgNum-topmailnum,emailMsgNum):  
        for mail in pop3.retr(i+1)[1]:  
            if mail.startswith('Date'):  
                try:
                    data = time.strptime(mail.replace("Date: ",'')[4:24], '%d %b %Y %H:%M:%S')  
                except: data = time.strptime(mail.replace("Date: ",'')[5:25], '%d %b %Y %H:%M:%S')
            if mail.startswith('Subject'):  
                mail = mail.replace('Subject: ','')
                if "?=" in mail:
                    if 'gb2312' in mail:
                        mail = p.sub('',mail)
                        mail = mail.replace('?=','')
                        mail = base64.decodestring(mail)
                        subject = mail 
                    if 'utf-8' in mail:
                        mail = p.sub('',mail)
                        mail = mail.replace('?=','')
                        mail = base64.decodestring(mail) 
                        subject = mail.decode("utf8")
                else:subject = mail
        mails.append((data,subject))
    # 退出
    pop3.quit()
    return mails
#for i in  get_mail_info("popcom.263xmail.com","jiangxiaohu@1218.com.cn","Rzx123"):
#    print time.strftime('%Y-%m-%d %H:%M:%S',Public.date_add(time.mktime(i[0]), h=8)),i[1]