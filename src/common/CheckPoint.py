#!/usr/bin/python
#coding=utf8

'''
Created on 2013-5-14

@author: zengchaoping
'''
#from BeautifulSoup import BeautifulSoup 
# from bs4 import BeautifulSoup,Tag,CData
import httplib,codecs,re,time,urllib,urllib2
from HTMLParser import HTMLParser
from decimal import *
from config.read_config import config
import getmail
from selenium import webdriver
import codecs,re,traceback
from selenium.common.exceptions import NoSuchElementException

def is_element_present(driver, how, what):
    try: driver.find_element(by=how, value=what)
    except NoSuchElementException, e: return False
    return True

def is_text_present(elementText,checkText):
    try:
        if checkText in elementText:
            return True
        else:
            return False
    except NoSuchElementException:
        traceback.print_exc()
        return False

    
def verification(CheckPoint,ExpectedR,ActualR,Errors):
    ExpectedR,ActualR = str(ExpectedR),str(ActualR)
    
#     codecs.register_error("cjk_replace", cjk_replace)
    #过滤空白字符
    p1 = re.compile("\s")
    #过滤HTML代码
    p2 = re.compile("<.+?>")
#    #过滤HTML空格
#    p3 = re.compile("&nbsp;")
#    p4 = re.compile("&#.+?;")
#     if ExpectedR!='' and ActualR!='':
#         expect = p2.sub('',p1.sub('',str(ExpectedR)))
#         actual = p2.sub('',p1.sub('',str(ActualR)))
#         if expect in actual:
#             expect = actual
#     else:
#         expect = ExpectedR.replace(' ','')
#         actual = ActualR.replace(' ','')
    if ExpectedR == ActualR:
        print '%s   验证通过：<br>       预期结果(%s); 实际结果(%s)'%(CheckPoint,ExpectedR,ActualR)     
    else:
        print '<B style="color: red;">%s   验证失败：<br>      预期结果(%s);实际结果(%s)</B>'%(CheckPoint,ExpectedR,ActualR)
        Errors.append('error')
        
def Verification(CheckPoint,ExpectedR,ActualR,Errors):
    ExpectedR,ActualR = str(ExpectedR),str(ActualR)
#     codecs.register_error("cjk_replace", cjk_replace)
    #过滤空白字符
    p1 = re.compile("\s")
    #过滤HTML代码
    p2 = re.compile("<.+?>")
    #过滤HTML空格
    p3 = re.compile("&nbsp;")
    p4 = re.compile("&#.+?;")
    if ExpectedR!='' and ActualR!='':
        expect = p4.sub("",p3.sub('',p2.sub('',p1.sub('',str(ExpectedR)))))
        actual = p4.sub("",p3.sub('',p2.sub('',p1.sub('',str(ActualR)))))
        if expect in actual:
            expect = actual
    else:
        expect = ExpectedR.replace(' ','')
        actual = ActualR.replace(' ','')
    if expect == actual:
        print '%s   验证通过：<br>       预期结果(%s); 实际结果(%s)'%(CheckPoint,str(expect),str(actual))     
    else:
        print '<b style="color: red;">%s   验证失败：<br>      预期结果(%s);实际结果(%s)</b>'%(CheckPoint,str(expect),str(actual))
        Errors.append('error')

# def is_alert_present(self):
#     try: self.driver.switch_to_alert()
#     except NoAlertPresentException as e: return False
#     return True

def close_alert_and_get_its_text(self):
    try:
        alert = self.driver.switch_to_alert()
        alert_text = alert.text
        if self.accept_next_alert:
            alert.accept()
        else:
            alert.dismiss()
        return alert_text
    finally: self.accept_next_alert = True

def Verif_for_strinstr(CheckPoint,ExpectedR,ActualR,Errors):
    if ExpectedR in ActualR:
        print u'%s   验证通过：<br>       预期结果(%s); 实际结果(%s)'%(CheckPoint,ExpectedR,ActualR)     
    elif ActualR in ExpectedR:
        print u'%s   验证通过：<br>       预期结果(%s); 实际结果(%s)'%(CheckPoint,ExpectedR,ActualR)     
    else:
        print u'<b style="color: red;">%s   验证失败：<br>      预期结果(%s);实际结果(%s)</b>'%(CheckPoint,ExpectedR,ActualR)
        Errors.append('error')

        
def JudgePass(self,caseName):
    if len(self.Errors)>0:
        print u'\n%s测试用例不通过!,一共有 %s 个验证点验证不通过.'%(caseName,len(self.Errors))
    else:print u'%s测试用例通过！'%(caseName)
    self.assertEqual(0,len(self.Errors))
    

def Deviation_Verifi(CheckPoint,expect,actual,Errors,std=0.05):
    expect = Decimal(expect)
    actual = Decimal(actual)
    if Decimal((expect+actual)/2)>0:
        std1 = abs(expect-actual)/Decimal((expect+actual)/2)
    else:std1=0
    if std1<std:
        print '%s   验证通过，误差小于%s<br />       预期结果(%s); 实际结果(%s)'%(CheckPoint,std,str(expect),str(actual))     
    elif abs(expect-actual)<=2:
        print '%s   验证通过，误差小于%s<br />       预期结果(%s); 实际结果(%s)'%(CheckPoint,std,str(expect),str(actual))     
    else:
        print '<b style="color: red;">%s   验证失败，误差大于%s<br />      预期结果(%s);实际结果(%s)</b>'%(CheckPoint,std,str(expect),str(actual))
        Errors.append('error')


#通过邮件发送时间和主题验证邮件是否发送成功

# def verf_sendmail(server, user, password,Subject,MailDate,Errors):
#     mails = getmail.get_mail_info(server, user, password, 5)
#     num = 0
#     for subj,date in mails:
#         senddate = time.strftime('%Y-%m-%d %H:%M',date_add(time.mktime(subj), h=8))
#         if subj == Subject and date>=senddate:
#             num=num+1
#     if num!=0:
#         print u'报表邮件发送验证通过：<br />       预期结果(目的邮箱收到主题为"%s"的邮件); 实际结果(目的邮箱收到主题为%s的邮件)'%(Subject,Subject)
#     else:
#         print u'<b style="color: red;">报表邮件发送验证失败:<br />      预期结果(目的邮箱收到主题为"%s"的邮件); 实际结果(目的邮箱未收到主题为"%s"的邮件)</b>'%(Subject,Subject)
#         Errors.append('error')
        
        
       
        
        
        
        
        
        
        
        
        