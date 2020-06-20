#!/usr/bin/python3
#encoding:utf-8
'''
@File    :   main.py
@Time    :   2020/05/17 15:35:04
@Author  :   Kevin Lau 
@Version :   1.0
@Contact :   kevinlaulk@162.com
@WebSite :   www.github.com/kevinlaulk
'''
# 主目录 需要chrome 提交至github版本


import os, time
from spiderhelper import SpiderHelper
import OCRapi

if __name__ == '__main__':


    url = 'http://xgsys.swjtu.edu.cn/SPCP/Web/UserLogin.aspx'
    # 建立类对象
    spider1 = SpiderHelper()
    # 访问链接
    respcontent = spider1.Response(url)
    print(type(respcontent))
    # html写入txt
    basePath = os.getcwd()
    spider1.RespReadTXTWrite(basePath + '\\data\\response.txt')


    #填学号并登录
    spider1.SeleniumLogStartByEdge(url)  # 要填表单必须用seleniumlog  模拟手机端登录去除验证码
    spider1.SeleniumFindId('StudentId')
    spider1.SeleniumTargetSendKeys('2017200413')
    spider1.SeleniumFindId('Name')
    spider1.SeleniumTargetSendKeys(r'刘凯')
    spider1.SeleniumFindId('IdCard')
    spider1.SeleniumTargetSendKeys('131457')
    # 截取验证码识别
    spider1.SeleniumScreenShot('code-img')
    captcha_str = OCRapi.base64_api("./data/screenshot/captcha.jpg")
    spider1.SeleniumFindId('codeInput')
    spider1.SeleniumTargetSendKeys(captcha_str)
    spider1.SeleniumFindId('Submit')
    spider1.SeleniumTargetClick()

    # 学生健康填报
    respcontent = spider1.SeleniumJumpTONewPage()
    spider1.RespReadTXTWrite(basePath + '\\data\\newresponse.txt')
    #打开健康填报
    xpathdir = '//div[@class="plat-title" and contains(text(),"学生健康情况填报")]'
    result = spider1.SeleniumFindXpath(xpathdir)
    print(result)
    # spider1.SeleniumFindClass('plat-title')
    spider1.SeleniumTargetClick()

    # 跳转新页面，定位进度
    respcontent = spider1.SeleniumJumpTONewPage()
    spider1.RespReadTXTWrite(basePath + '\\data\\tianbaoresponse.txt')
    # 打开返校申请
    spider1.SeleniumFindId('ckCLS')
    spider1.SeleniumTargetClick()
    # 跳转新页面，定位进度
    respcontent = spider1.SeleniumJumpTONewPage()
    spider1.SeleniumFindId('save_form')
    spider1.SeleniumTargetClick()
    print(result)

    time.sleep(10)
    spider1.SeleniumQuit()

    '''
    # 返校申请
    # 跳转新页面，定位进入返校申请
    respcontent = spider1.SeleniumJumpTONewPage()
    spider1.RespReadTXTWrite(basePath + '\\data\\newresponse.txt')
    #打开返校申请
    xpathdir = '//div[@class="plat-title" and contains(text(),"返校申请")]'
    result = spider1.SeleniumFindXpath(xpathdir)
    print(result)
    # spider1.SeleniumFindClass('plat-title')
    spider1.SeleniumTargetClick()

    # 跳转新页面，定位进度
    respcontent = spider1.SeleniumJumpTONewPage()
    spider1.RespReadTXTWrite(basePath + '\\data\\shenheresponse.txt')
    # 打开返校申请
    xpathdir = '//body/div/div/pre/text()'
    result = spider1.XpathCompile(xpathdir)
    print(result)

    time.sleep(10)
    spider1.SeleniumQuit()
    '''



    '''
    # 解析目标1
    xpathdir = '//body/div/div/pre/text()'
    items = spider1.XpathCompile(xpathdir)
    for item in items:
        spider1.TxtWrite(item+'\n', './data/title.txt')
    # 解析目标2
    xpathdir = '//a[@target="_blank" and @class="title"]/@href'
    items = spider1.XpathCompile(xpathdir)
    for item in items:
        spider1.TxtWrite(item+'\n', './data/url.txt')

    # 下载图片
    spider1.SeleniumLogStart(url)
    spider1.SeleniumRollSmooth()
    spider1.SeleniumResponse()
    xpathdir = '//img[@alt and @src]/@src'
    items = spider1.XpathCompile(xpathdir)
    name = 1
    for item in items:
        print(item)
        spider1.WebpWrite(item, './data/JPEG/'+str(name)+'.png')
        name = name + 1
        # print(item)
    
    '''