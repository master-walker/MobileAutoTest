#!/usr/bin/env python
# coding=utf-8
'''
Created on 2011-5-25
@author: jxh
Description:公共参数配置和公共函数模块

'''
import httplib
import logging.config
import re
import time
import urllib
import urllib2
from HTMLParser import HTMLParser

from appium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver
from config.read_config import config


# 获取driver
def getDriver():
    desired_caps = {}
    desired_caps['platformName'] = config.platformName
    desired_caps['platformVersion'] = config.platformVersion
    desired_caps['deviceName'] = config.deviceName
    desired_caps['appPackage'] = config.appPackage
    desired_caps['appActivity'] = config.appActivity

    driver = webdriver.Remote(config.command_executor, desired_caps)
    return driver


# 获取日志记录器
def get_logger():
    logging.config.fileConfig("../config/logConf.ini")
    logger = logging.getLogger()
    return logger


def getActivityResource(driver):
    return driver.getPageResource()


# 字符转码异常处理
def cjk_replace(exc):
    if not isinstance(exc, UnicodeDecodeError):
        raise TypeError("don't know how to handle %r" % exc)

    if exc.end + 1 > len(exc.object):
        raise TypeError('unknown codec ,the object too short!')

    ch1 = ord(exc.object[exc.start:exc.end])
    newpos = exc.end + 1
    ch2 = ord(exc.object[exc.start + 1:newpos])
    sk = exc.object[exc.start:newpos]

    if 0x81 <= ch1 <= 0xFE and (0x40 <= ch2 <= 0x7E or 0x7E <= ch2 <= 0xFE):  # GBK
        return (unicode(sk, 'cp936'), newpos)

    if 0x81 <= ch1 <= 0xFE and (0x40 <= ch2 <= 0x7E or 0xA1 <= ch2 <= 0xFE):  # BIG5
        return (unicode(sk, 'big5'), newpos)

    raise TypeError('unknown codec !')


def get_json(host, param):
    json_url = 'http://%s/system/protocol/list/format/json' % host
    params = (('node', param),)
    # group_2
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 5.1; rv:5.0) Gecko/20100101 Firefox/5.0')]

    jsons = urllib2.Request(json_url, urllib.urlencode(params))
    datas = urllib2.urlopen(jsons).read()

    def custom_eval(str):
        str = str.replace("true", "\"true\"")
        str = str.replace("null", "\"null\"")
        str = str.replace("false", "\"false\"")
        return eval(str)

    datas = custom_eval(datas)
    result = []
    for i in datas:
        temp = []
        temp.append(i['id'])
        temp.append(i['value'])
        temp.append(eval('u"' + i['text'] + '"'))
        temp.append(eval('u"' + i['leaf'] + '"'))
        result.append(temp)
    return result


def date_add(date=time.time(), d=0, h=0, m=0, s=0):
    if type(date) is str:
        if ':' in date:
            date = time.strptime(date, '%Y-%m-%d %H:%M:%S')
        else:
            date = time.strptime(date, '%Y-%m-%d')
        date = time.mktime(date)
    date = date + d * 24 * 60 * 60 + h * 60 * 60 + m * 60 + s
    return time.localtime(date)


# 获取页面数据记录数
def get_page_rows(url):
    for i in range(60):
        try:
            if isinstance(url, WebDriver):
                url.switch_to_default_content()
                url.switch_to_frame(url.find_element_by_id("mainFrame"))
                s = url.find_element_by_xpath("//*[@id='ext-comp-1021']").text
                time.sleep(3)
                print s
                if s == "没有项目可显示":
                    page_rows = 0
                else:
                    page_rows = re.findall('\d-\d+', s)[0].replace('1-', '')
            break
        except:
            pass
        time.sleep(1)
    else:
        page_rows = 0

    return page_rows


# 获得远程WEB服务器时间
def get_webservertime(host, port='80'):
    conn = httplib.HTTPConnection(host + ':' + str(port))
    conn.request("GET", "/")
    r = conn.getresponse()
    # r.getheaders() #获取所有的http头
    ts = r.getheader('date')  # 获取http头date部分
    # 将GMT时间转换成北京时间
    ltime = time.strptime(ts[5:25], "%d %b %Y %H:%M:%S")
    return time.mktime(ltime) + 8 * 60 * 60


# 获取Linux服务器时间零点刻浮点时间
'''
def get_int_se_time(day=1):
    import RemoteOpt
    Re = RemoteOpt.remotehost(config.os_host,config.os_user,config.os_passwd)
    stdout,stderr = Re.exec_command("date +'%Y-%m-%d'")

    stime = time.mktime(time.strptime(stdout+"00:00:00","%Y-%m-%d %H:%M:%S"))-(day*24*60*60)
    etime = time.mktime(time.strptime(stdout+"23:59:59","%Y-%m-%d %H:%M:%S"))-(day*24*60*60)
    Re.close()
    return int(stime),int(etime)
'''


# 将整数转换成时分秒
def int_to_time(num):
    h = num / 60 / 60
    m = (num - h * 60 * 60) / 60
    s = (num - h * 60 * 60 - m * 60) % 60
    return '%02d:%02d:%02d' % (h, m, s)


# 将字典的key和value互换，返回一个新的字典
def dic_reversal(dic1):
    dic2 = {}
    for key in dic1.keys():
        dic2[dic1[key]] = key
    return dic2


def setYesterday(sel):
    sel.click("css=#sdate+img")
    time.sleep(1)
    sel.click("css=td:has(+td[title='今天']) span")
    sel.assign_id("css=td:has(+td[title='今天'])", "test1")
    time.sleep(1)
    sel.click("css=#edate+img")
    time.sleep(1)
    sel.click("css=td:has(+td[title='今天']):not(#test1) span")
    time.sleep(1)


# 去除 html 标签
def strip_tags(html):
    html = html.strip()
    html = html.strip("\n")
    result = []
    parse = HTMLParser()
    parse.handle_data = result.append
    parse.feed(html)
    parse.close()
    return "".join(result)


# if __name__ == "__main__":
#     driver = getDriver()
