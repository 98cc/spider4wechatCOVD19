#!/usr/bin/env python
# coding:utf-8

'''
Created on 2020-3-19
@author: kevin
'''
import os,time
from spiderhelper import SpiderHelper

url = 'https://www.bilibili.com/ranking'
test = SpiderHelper()
test.SeleniumLogStart(url)

js = 'var action=document.documentElement.scrollTop=100'
# 设置滚动条距离顶部的位置，设置为 10000， 超过10000就是最底部
for item in range(1,1000):
    print(item)
    test.SeleniumExecute('var action=document.documentElement.scrollTop=' + str(100*item))  # 执行脚本

print(test.SeleniumResponse())
# target = test.SeleniumFindXpath('//div[@class="num" and text()=' + str(70) + ']')
# response = test.SeleniumRoll2Target(target)
# print(response)
