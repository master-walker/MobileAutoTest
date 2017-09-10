#!/usr/bin/python
# coding=utf-8
'''
Created on 2016-11-22
@author: 
Description:批量执行测试用例，并输出测试报告的模块
为了能单独执行此文件，需手动导入目录路径到sys.path
'''


import sys, os
import unittest, time, threading, multiprocessing
from common import HTMLTestRunner
from execute_script import test_home_page

src_path = os.path.abspath('..')
sys.path.append(src_path)
reload(sys)


def create_suite():
    testunit = unittest.TestSuite()
    testcase_path = r"."
    discover = unittest.defaultTestLoader.discover(testcase_path, pattern="test*.py", top_level_dir=None)
    for test_suite in discover:
        for test_case in test_suite:
            testunit.addTests(test_case)

    return testunit


def suite():
    return unittest.TestSuite(( \
        #                                 unittest.makeSuite(TestCase.TestCase),
        #                                 unittest.makeSuite(TestBaseInfoManage.TestBaseInfoManage),
        #                                 unittest.makeSuite(TestMonitorTaskConfig.TestCase),
        unittest.makeSuite(test_home_page.TestHomePage)
    ))


def run_suite(suite):
    report_dir_path = os.path.abspath('../report/%s' % (time.strftime("%Y-%m-%d", time.localtime())))
    if os.path.exists(report_dir_path) is not True:
        os.mkdir(report_dir_path)
    print report_dir_path
    report_file_path = report_dir_path + u"/AutoTestReport-%s.html" % (time.strftime(u"%H-%M", time.localtime()))
    fp = open(report_file_path, 'wb')
    #     for case in suite:
    runner = HTMLTestRunner.HTMLTestRunner(
        stream=fp,
        title='Gcall自动化测试结果',
        description='Gcall自动化测试用例执行结果'
    )
    #         proc=multiprocessing.Process(target=runner.run(case),args=(case,))
    #         proc=threading.Thread(target=runner.run,args=(case,))
    #         procList.append(proc)
    #         for proc in procList:
    #             proc.start()
    #         for proc in procList:
    #             proc.join()
    #             time.sleep(5)
    runner.run(suite)
    fp.close()


if __name__ == "__main__":
    #     suite=create_suite()
    #     suite=suite()
    run_suite(create_suite())









    #     zfile = '%sSystemManage.zip'%(time.strftime("%Y%m%d",time.localtime()))
    #
    #     #创建压缩文件
    #     z = OperFile.ZFile(zfile, 'a')
    #     z.addfile(report_path)
    #     z.close()
    #     '''
    #     add in 20160928
    #     '''
    #     files = [os.path.abspath(zfile)]
    #     to= ['wangling2@1218.com.cn','wangling2@1218.com.cn']
    #     subject="testxxxx"
    # sendreport.SendReport(u'报表管理自动化测试报告', to, files)
