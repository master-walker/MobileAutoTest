#!/usr/bin/python
#coding=cp936
'''
Created on 2011-8-16
@author: jxh
Description:

'''

import os,time,sys
src_path = os.path.abspath('..')
sys.path.append(src_path)
reload(sys)

from common import sendmail
report_path = time.strftime("%Y-%m-%d",time.localtime())

##����ܹ�ִ�е�py�ļ�
#flist = []
#for py in os.listdir('.'):
#    if 'py' in py and py != '__init__.py' and py != 'sendreport.py':
#        flist.append(py)
#pyfiles = ','.join(flist)

##�õ�����ľ���·��
#files = []
#for i in os.listdir('.'):
#    if '.zip' in i:
#        files.append(i)

def SendReport(subject,to,files):
    #�����ʼ�
    fro = 'xielisha@mail.87.com'
    #to = ['mail_spam@126.com','zengchaoping@1218.com.cn','shenzhijie@1218.com.cn','zhaohe@1218.com.cn']
    #smtpcom.263xmail.com
    mailserver = 'mail.87.com'
    user = 'xielisha@mail.87.com'
    passwd = 'lisha@123'
    sendmail.send_mail({'host':mailserver,'user':user,'passwd':passwd},fro, to,\
                        subject, u'<br>���û����ȸ��������<br>----------------------<br><font size="2bt">���ʼ�Ϊ�����Զ�����</font>',files)
    
    #ɾ��ѹ���ļ�
    for i in files:
        os.remove(i)
