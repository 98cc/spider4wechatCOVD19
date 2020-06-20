#!/usr/bin/env python
# coding:utf-8

'''
Created on 2020-3-19
@author: kevin
this version is for edge rather than chrome
'''

import urllib
# urllib2 = urllib.request
import urllib.request
from urllib import request
import re, os, sys, io, logging
from lxml import etree
from PIL import Image
from selenium import webdriver
from io import BytesIO
from time import sleep
import requests

class SpiderHelper(object):

    def __init__(self):
        #定义类变量
        self.datapath = './data/'
        self.scriptpath = ''
        self.outpath = './output/'
        self.url = ''
        self.respread = ''  # the read content of url response
        self.resp = ''
        self.cookie = ''

    def Response(self, url):
        self.url = url
        # 发送请求request
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}
        req = request.Request(url=url, headers=headers)
        # 接受相应response
        self.respread = request.urlopen(req).read()
        # print(self.respread.read().decode('utf-8'))
        return self.respread

    def CookieLogResponse(self, cookie, url):
        self.url = url
        self.cookie = cookie
        # 登录后才能访问的网站url
        # 浏览器登录后得到的cookie(即时)，也就是刚才复制的字符串
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf8')  # 改变标准输出的默认编码
        req = request.Request(url)
        # 设置cookie
        req.add_header('cookie', cookie)
        # 设置请求头
        req.add_header('User-Agent',
                       'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36')

        self.respread = request.urlopen(req).read()
        print(self.respread.decode('utf-8'))
        return self.respread

    def SeleniumLogStartByEdge(self, url):
        # 登陆chrome， 返回对象供外部使用（按键、输入、登陆）
        self.url = url
        # driver = webdriver.Chromedriver()
        # driver = webdriver.Chrome(executable_path=r"F:\工作\python\spider4wechatCOVD19\chromedriver.exe")  #chrome
        driver = webdriver.Edge("C:\ProgramData\Anaconda3\msedgedriver.exe")  #edge
        # driver = webdriver.Ie()
        driver.get(url)
        # driver.implicitly_wait(3) 等待打开时间
        self.driver = driver
        return driver

    def SeleniumLogStartByIphoneXChrome(self, url):
        # 登陆chrome， 返回对象供外部使用（按键、输入、登陆）
        self.url = url
        # driver = webdriver.Chromedriver()
        mobilesetting = {"deviceName": "iPhone X"}
        options = webdriver.ChromeOptions()  # 选项
        options.add_experimental_option("mobileEmulation", mobilesetting)  # 模拟手机
        driver = webdriver.Chrome(firefox_options=options, executable_path="C:\ProgramData\Anaconda3\chromedriver.exe")  # 配置参数

        # driver = webdriver.Edge(r"F:\工作\python\spider4wechatCOVD19\msedgedriver.exe")
        driver.get(url)
        # driver.implicitly_wait(3) 等待打开时间
        self.driver = driver
        return driver

    def SeleniumLogStartByIphoneXFirefox(self, url):
        # 登陆chrome， 返回对象供外部使用（按键、输入、登陆
        self.url = url
        # driver = webdriver.Chromedriver()
        # mobilesetting = {"deviceName": "iPhone X"}
        # options = webdriver.FirefoxOptions()  # 选项
        # options.add_argument("mobileEmulation", mobilesetting)  # 模拟手机
        capabilities = {'browserName': 'firefox',
            'firefoxOptions': {
                'mobileEmulation': {
                    'deviceName': 'iPhone X'
                }
            }
        }
        driver = webdriver.Firefox(desired_capabilities=capabilities, executable_path="C:\ProgramData\Anaconda3\geckodriver.exe")  # 配置参数
        # driver = webdriver.Edge(r"F:\工作\python\spider4wechatCOVD19\msedgedriver.exe")
        driver.get(url)
        # driver.implicitly_wait(3) 等待打开时间
        self.driver = driver
        return driver

    def SeleniumExecute(self, js):
        # 执行脚本（滚动进度条）
        # js = 'var action=document.documentElement.scrollTop=100'
        self.driver.execute_script(js) #执行脚本
        self.driver.implicitly_wait(3)

    def SeleniumResponse(self):
        # 随时返回html
        self.respread = self.driver.page_source
        return self.respread

    def SeleniumFindXpath(self, xpath):
        # 以xpath寻找， 返回寻找到的元素
        self.target = self.driver.find_element_by_xpath(xpath)
        return self.target

    def SeleniumFindClass(self, classname):
        # 以xpath寻找， 返回寻找到的元素
        self.target = self.driver.find_element_by_class_name(classname)
        return self.target

    def SeleniumRoll2Target(self, target):
        # 以某一元素对象为目标滚动进度条
        self.driver.execute_script("arguments[0].scrollIntoView();", target)
        self.respread = self.driver.page_source  # 返回html
        return self.respread

    def SeleniumRollSmooth(self, num=200):
        # 自动滚动进度条，解决图片慢加载问题(lazy image)
        js = 'var action=document.documentElement.scrollTop=100'
        # 设置滚动条距离顶部的位置，设置为 10000， 超过10000就是最底部
        for item in range(1, num):
            print("滚动进度条中>>>")
            self.SeleniumExecute('var action=document.documentElement.scrollTop=' + str(100 * item))  # 执行脚本

    def SeleniumScreenShot(self, imgclassname):
        self.driver.get_screenshot_as_file('./data/screenshot/screen.jpg')
        # 定位验证码元素坐标和大小
        location = self.driver.find_element_by_class_name(imgclassname).location
        size = self.driver.find_element_by_class_name(imgclassname).size
        # 通过验证码元素位置和长宽计算出矩形区域
        left = location['x']
        top = location['y']
        right = left + size['width']
        bottom = top + size['height']
        # 裁剪存储验证码图片，调用识别模块
        im = Image.open('./data/screenshot/screen.jpg')
        captcha = im.crop((left, top, right, bottom))
        captcha = captcha.convert('RGB')
        captcha.save('./data/screenshot/captcha.jpg')

    
    def SeleniumQuit(self):
        # 退出chrome
        self.driver.quit()

    def ReCompile(self, restring):
        # 正则匹配需求信息
        # 正则匹配需求字符串restring
        pattern = re.compile(restring)
        # 开始匹配，输出字符串数组items
        items = re.findall(pattern, self.respread)
        if items:
            print('the title and URL has been spided')

        # TODO
        # 例如将匹配信息输出至txt
        # path = 'title_URL'
        # for item in items:
        #     # print(str(type(item)) + str(type(items)))
        #     # print(items)
        #     # print(item[1] + item[0])
        #     if not os.path.exists(path):
        #         os.makedirs(path)
        #     title_URL_path = path + '/' + item[1] + '.txt'
        #     with open(title_URL_path, 'w') as f:
        #         f.write(item[0])
        return items

    def XpathCompile(self, xpathdir):
        # html = etree.parse(self.respread)
        html = etree.HTML(self.respread)
        # html = etree.HTML(self.respread.decode('utf-8')) 也可
        # 显示xml
        result = etree.tostring(html)
        # print(result.decode('utf-8'))

        # xpath过滤xml
        # TODO
        items = html.xpath(xpathdir)
        # 例如简单匹配案例
        # anno_name = html.xpath('//object/name')
        # anno_xmin = html.xpath('//object//bndbox/xmin')
        # anno_ymin = html.xpath('//object//bndbox/ymin')
        # anno_xmax = html.xpath('//object//bndbox/xmax')
        # anno_ymax = html.xpath('//object//bndbox/ymax')
        # name = [x.text for x in anno_name]
        # xmin = [int(x.text) for x in anno_xmin]
        # ymin = [int(x.text) for x in anno_ymin]
        # xmax = [int(x.text) for x in anno_xmax]
        # ymax = [int(x.text) for x in anno_ymax]
        return items

    def SeleniumTargetSendKeys(self,  SendKey):
        self.target.send_keys(SendKey)
        print(SendKey + 'has been sent')

    def SeleniumFindId(self, id):
        # 以id寻找， 返回寻找到的元素
        self.target = self.driver.find_element_by_id(id)
        return self.target

    def SeleniumFindName(self, name):
        # 以id寻找， 返回寻找到的元素
        self.target = self.driver.find_element_by_name(name)
        return self.target

    def SeleniumTargetClick(self):
        self.target.click()
        print('has been clicked')

    def SeleniumJumpTONewPage(self):
        sleep(1)
        NewWindow = self.driver.current_window_handle # 此行代码用来定位当前页面
        #已将driver刷新，可使用
        self.respread = self.driver.page_source.encode()
        return self.respread

        # time.sleep(1) 一定要加
        # driver.switch_to.window(driver.window_handles[0])

    def AnnoRead(self):
        # 检查Annotations是否存在
        if not os.path.exists(self.datapath):
            print('the Annotations is not exis')
        else:
            self.Annolist = os.listdir(self.datapath)
            print('the amount is :%s' % len(self.Annolist))
            print(self.Annolist)

    def XmlRead(self):
        for itemxml in self.Annolist:
            self.xmldir = os.path.join(self.datapath, itemxml)
            print('opening the xmlfile:%s' % self.xmldir)
            self.html = etree.parse(self.xmldir)
            # 显示xml
            # result = etree.tostring(self.html)
            # print(result)
            # xpath 提取path
            filepath = self.html.xpath('//path')
            print(filepath[0].text)
            # 正则表达式提取子路径
            pattern = re.compile(
                r'\\([\d|\w|_]*)\\([\d|\w|_]*)\\([\d|\w|_]*.jpg)$')
            items = re.findall(pattern, filepath[0].text)
            if not items:
                print('xml path is not found')
            else:
                # print(items[0][1])
                changepath = '/home/' + str(items[0][0]) + '/' + str(items[0][1]) + '/' + str(items[0][2])
                print(changepath)
                # 修改节点内容
                self.html.xpath('//path')[0].text = changepath
                if not os.path.exists(self.outpath):
                    print('the output dir is not exis')
                else:
                    outputdir = os.path.join(self.outpath, itemxml)
                    self.html.write(outputdir)

    def CropImg(self, imgpath, imgname, cropname, xmin, ymin, xmax, ymax):
        # 查找cropname中的重复元素
        # setcropname = list(set(cropname))
        # for itemset in setcropname:
        # 	if cropname.count(itemset) > 1:
        # 		# itemset 有多个
        target = 'Brace_sleeve_screw'
        im = Image.open(imgpath)
        i = 0
        j = 0
        cropnamelist = []
        for i, itemname in enumerate(cropname):
            if target == itemname:
                print(itemname)
                cropbox = (xmin[i], ymin[i], xmax[i], ymax[i])
                region = im.crop(cropbox)
                region = region.resize((80, 80))
                basepath = '../data/output/'
                addpath = basepath + itemname
                if not os.path.exists(addpath):
                    os.makedirs(addpath)
                if cropname in cropnamelist:
                    # 有重复命名
                    j += 1
                    fullpath = os.path.join(addpath, imgname + '_' + str(j) + '.jpg')
                else:
                    fullpath = os.path.join(addpath, imgname + '_0' + '.jpg')
                cropnamelist.append(cropname)
                region.save(fullpath)

    def RespReadTXTWrite(self, txtoutpath):
        dirname = os.path.dirname(txtoutpath)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        # 无txt文件自动创建
        with open(txtoutpath, 'wb') as f:
            f.write(self.respread)

    def TxtWrite(self, txtcontent, txtoutpath):
        dirname = os.path.dirname(txtoutpath)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        # 无txt文件自动创建
        with open(txtoutpath, 'a', encoding='utf-8') as f:
            f.write(txtcontent)

    def JpegWrite(self, jpegurl, jpegoutpath):
        # 创建目录
        dirname = os.path.dirname(jpegoutpath)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        # 无文件自动创建
        print('downloding: %s' % jpegurl)
        # 下载图片至指定目录
        try:
            urllib.request.urlretrieve(jpegurl, jpegoutpath)
            # urllib.request.urlretrieve(jpegurl, 'image/%s%s' % (item[0], os.path.splitext(item[1])[1]))
        except BaseException as e:
            logging.exception(e)  # 错误继续
            print(e)  # 错误停滞

    def WebpWrite(self, url, jpegoutpath):


        res = requests.get(url, stream=True)  # 获取字节流最好加stream这个参数,原因见requests官方文档

        byte_stream = BytesIO(res.content)  # 把请求到的数据转换为Bytes字节流(这样解释不知道对不对，可以参照[廖雪峰](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000/001431918785710e86a1a120ce04925bae155012c7fc71e000)的教程看一下)

        roiImg = Image.open(byte_stream)  # Image打开Byte字节流数据
        # roiImg.show()   #  弹出 显示图片
        imgByteArr = io.BytesIO()  # 创建一个空的Bytes对象

        roiImg.save(imgByteArr, format='PNG')  # PNG就是图片格式，我试过换成JPG/jpg都不行

        imgByteArr = imgByteArr.getvalue()  # 这个就是保存的图片字节流

        # 创建目录
        dirname = os.path.dirname(jpegoutpath)
        if not os.path.exists(dirname):
            os.makedirs(dirname)
        # 无文件自动创建
        print('downloding: %s' % url)
        # 下载图片至指定目录

        with open(jpegoutpath, "wb") as f:
            f.write(imgByteArr)