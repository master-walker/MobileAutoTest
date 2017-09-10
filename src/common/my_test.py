##!/usr/bin/env python
# coding=utf-8
'''
Created on 2017年5月29日

'''

import unittest
from common import public


class MyTest(unittest.TestCase):
    """
    The base class is for all testcase.
    """

    def setUp(self):
        self.logger = public.get_logger()
        self.driver = public.getDriver()
        self.logger.info("\n")
        self.logger.info('############################### START ###############################')

    def tearDown(self):
        self.driver.quit()
        self.logger.info('###############################  End  ###############################')
