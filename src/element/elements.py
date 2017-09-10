#!/usr/bin/env python
# coding=utf-8
'''
Created on 2017年4月2日

@author: Master Skywalker
'''
from selenium.webdriver.common.by import By


class LoginPageLocators(object):
    userNameInputBox = (By.ID, "com.gcall.sns:id/et_username", "用户名")
    passwdInputBox = (By.ID, "com.gcall.sns:id/et_password", "密码")
    loginBtn = (By.ID, "com.gcall.sns:id/btn_login", "登录")

    # 登录页面元素
    loginElements = [userNameInputBox, passwdInputBox, loginBtn]


# 首页
class HomePageLocators(object):
    postBtn = (By.XPATH, "//android.widget.TextView[contains(@text,'发帖')]", "发帖")
    postInputBox = (By.XPATH, "//android.widget.EditText[contains(@text,'说点什么')]", "发帖输入框")
    submitBtn = (By.XPATH, "//android.widget.TextView[contains(@text,'发布')]", "发布")
    # 发布动态的元素
    postedElements = [postInputBox, submitBtn]


# 主页
class PersonalPageLocators(object):
    personalPageBtn = (By.XPATH, "//android.widget.TextView[contains(@text,'主页')]", "主页")
    subMenuImgBtn = (By.ID, "com.gcall.sns:id/iv_circle_menu", "下拉按钮")


# enterBlogElements=[personalCardBtn,blogBtn]

class PopWindowLocators(object):
    # 删除按钮
    delBtn = (By.XPATH, "//android.widget.TextView[contains(@text,'删除')]", "删除")
