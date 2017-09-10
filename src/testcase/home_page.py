#!/usr/bin/env python
# coding=utf-8

'''
Created on 2017年5月23日

@author: Master SkyWalker
'''

import time
from common import base_page
from element.elements import HomePageLocators


class HomePage(base_page.BasePage):
    def swipe_test(self):
        self.swipe_to_left(1080, 1920)
        time.sleep(2)
        self.swipe_to_right(1080, 1920)
        time.sleep(2)
        self.swipe_to_up(1080, 1920)
        time.sleep(2)
        self.swipe_to_down(1080, 1920)

    def test_all(self):
        self.take_screen_shot()
        print self.get_activity()
        print self.driver.is_app_installed("com.gcall.sns")
        print self.is_enabled(HomePageLocators.postInputBox)
        print self.is_displayed(HomePageLocators.postInputBox)
        print self.is_selected(HomePageLocators.postInputBox)
        # self.flick(750, 960, 250, 960)
        self.close_app()
        self.launch()
        self.background(3)
        self.open_notifications()
        self.lock(3)

    def posted(self):
        # 点击发帖输入框
        self.click(HomePageLocators.postInputBox)
        self.submit(HomePageLocators.postedElements, "test")
