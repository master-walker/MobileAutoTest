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
    # ����һ��pop3�������ʱ��ʵ�����Ѿ������Ϸ�������
    pop3 = poplib.POP3(server)
    # ���õ���ģʽ�����Կ�����������Ľ�����Ϣ
    #pp.set_debuglevel(1)
    # ������������û���
    pop3.user(user)
    # ���������������
    pop3.pass_(password)
    # ��ȡ���������ż���Ϣ��������һ������Ԫ�ص��б���һ����һ���ж��ٷ��ʼ����ڶ����ǹ��ж����ֽ�
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
    # �˳�
    pop3.quit()
    return mails
#for i in  get_mail_info("popcom.263xmail.com","jiangxiaohu@1218.com.cn","Rzx123"):
#    print time.strftime('%Y-%m-%d %H:%M:%S',Public.date_add(time.mktime(i[0]), h=8)),i[1]