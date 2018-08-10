#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time   : 2018/7/29 0029 20:25
# @Author : wangyulin
# @File   : 爬取小说.py
import requests
import linecache
import time
from bs4 import BeautifulSoup
from urllib import request, parse
import urllib.request
from tkinter.filedialog import askdirectory
# from bs4 import BeautifulSoup
from tkinter import *
# from lxml import etree
import os
import re
import threading


class MYapp(Tk):
    def __init__(self):
        super().__init__()
        self.wm_title('小说下载器 BY wangyulin')
        sw = self.winfo_screenwidth()
        # 得到屏幕宽度
        sh = self.winfo_screenheight()
        # 得到屏幕高度
        ww = 550
        wh = 415
        # 窗口宽高为100
        powx = (sw - ww) / 2
        powy = (sh - wh) / 2
        # self.iconbitmap('icons\\format.ico')
        self.geometry("%dx%d+%d+%d" % (ww, wh, powx, powy))
        self.resizable(width=False, height=False)  # 设置不可改变窗口大小
        self.attributes("-alpha", 1)  # 背景虚化
        self["bg"] = "white"  # 设置窗口的背景颜色
        self.protocol('WM_DELETE_WINDOW', self.destroy)  # 绑定窗口退出事件
        self.setupui()

    def dakai(self):
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            path = self.line
            os.startfile(path)
        else:
            path = os.path.abspath(os.curdir)
            os.startfile(path)

    @staticmethod
    def qingkong():
        MYapp.entry.delete('0', 'end')  # 清除文本框内容

    def setupui(self):  # 设置根窗口的UI
        lable = Label(self, text='请输入小说网页地址', font=('楷体', 20))
        lable.grid(row=0, column=0)
        MYapp.url = StringVar()  # 这即是输入框中的内容
        MYapp.entry = Entry(
            self, textvariable=MYapp.url, font=(
                '微软雅黑', 15), width=23)
        MYapp.entry.grid(row=0, column=1)
        MYapp.text = Listbox(self, font=('微软雅黑', 15), width=45, height=10)
        MYapp.text.grid(row=1, columnspan=2)
        button = Button(
            self, text='笔趣阁小说', font=(
                '微软雅黑', 15), command=download2)
        button.place(x=5, y=316.5, width=120, height=45)
        button = Button(
            self, text='海岸线小说', font=(
                '微软雅黑', 15), command=download)
        button.place(x=140, y=316.5, width=120, height=45)
        button = Button(
            self, text='搜索小说', font=(
                '微软雅黑', 15), command=download3)
        button.place(x=140, y=365, width=120, height=45)
        fu = local()
        button = Button(
            self, text='指定路径', font=(
                '微软雅黑', 15), command=fu.lujing)
        button.place(x=330, y=316.5, width=100, height=45)
        button = Button(
            self, text='开始下载', font=(
                '微软雅黑', 15), command=self.top)
        button.place(x=330, y=365, width=100, height=45)
        button = Button(
            self, text='清空地址栏', font=(
                '微软雅黑', 15), command=self.qingkong)
        button.place(x=5, y=365, width=120, height=45)
        button = Button(
            self, text='退出程序', font=(
                '微软雅黑', 15), command=self.destroy)
        button.place(x=445, y=365, width=100, height=45)
        button = Button(
            self, text='打开文件', font=(
                '微软雅黑', 15), command=self.dakai)
        button.place(x=445, y=316.5, width=100, height=45)

    def top(self):
        top = Toplevel(self)
        top.title('下载小说')
        sw = top.winfo_screenwidth()  # 得到屏幕宽度
        sh = top.winfo_screenheight()  # 得到屏幕高度
        ww = 260
        wh = 80
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        # self.iconbitmap('icons\\format.ico')
        # 图标
        top.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
        top.resizable(width=False, height=False)
        # 设置不可改变窗口大小
        top.attributes("-alpha", 1)
        # 背景虚化
        top["bg"] = "white"
        # 设置窗口的背景颜色
        top.protocol('WM_DELETE_WINDOW', top.destroy)
        # 绑定窗口退出事件
        lable = Label(top, text='输入小说序号', font=('微软雅黑', 15))
        lable.grid(row=0, column=0)
        Select.url3 = StringVar()
        Select.entry = Entry(
            top, textvariable=Select.url3, font=(
                '微软雅黑', 15))
        Select.entry.grid(row=0, column=1)
        button = Button(
            top, text='确定', font=(
                '微软雅黑', 12), command=download4)
        button.place(x=175, y=40, width=40, height=40)
        button = Button(
            top, text='取消', font=(
                '微软雅黑', 12), command=top.destroy)
        button.place(x=220, y=40, width=40, height=40)


class section:
    def onpaste(self):
        try:
            self.text = app.clipboard_get()
        except TclError:
            pass
        MYapp.url.set(str(self.text))

    def oncopy(self):
        self.text = MYapp.entry.get()
        app.clipboard_append(self.text)

    def oncut(self):
        self.oncopy()
        try:
            MYapp.entry.delete('sel.first', 'sel.last')
        except TclError:
            pass


class local:
    def __init__(self):
        super().__init__()

    @staticmethod
    def lujing():
        local.path_ = askdirectory()
        if os.path.exists(local.path_):
            with open('log.txt', 'w', encoding='utf-8') as fp:
                fp.write(local.path_)
        else:
            pass


class Select(Tk):
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        Select.url3 = StringVar()
        Select.entry = Entry(
            self, textvariable=Select.url3, font=(
                '微软雅黑', 15))
        Select.entry.grid(row=0, column=1)

class haianxian(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.url1 = MYapp.entry.get()
        self.xiaoshuo_id = self.url1.split('info/')[-1]
        if self.xiaoshuo_id == self.url1:
            self.new_url = self.xiaoshuo_id
        else:
            self.id = self.xiaoshuo_id.replace('.htm', '')
            self.new_url = 'https://www.haxds.com/files/article/html/{}/index.html'.format(
                self.id)

    def run(self):
        global x

        self.new_url3 = self.new_url.split('html')[0]
        if self.new_url3 != 'https://www.haxds.com/files/article/':
            MYapp.text.insert(END, '请输入正确地址')
            MYapp.text.see(END)
            MYapp.text.update()
        else:
            x = 0
            self.url_2 = self.get_url(self.new_url)
            for i in self.url_2[0]:
                test = self.download(i)
                c = str(x)
                a = c + '  ' + test[0]
                b = test[1]
                self.write(a, b)
                x += 1
            self.hebing()
            MYapp.text.insert(END, '合并成功')
            MYapp.text.see(END)
            MYapp.text.update()

    def get_url(self, url1):
        header = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'www.haxds.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/48.0.2564.116 Safari/537.36',
            'Connection': 'keep-alive',
            'Referer': 'https://www.haxds.com/'}

        self.html = requests.get(url1, headers=header).text
        req1 = '<h1>(.*?)</h1>'
        book_name = re.findall(req1, self.html)
        req2 = 'target="_blank">(.*?)</a>'

        author_name = re.findall(req2, self.html)
        for a in author_name:
            self.authorname = a
        for i in book_name:
            self.newname = i
        self.newwname = self.newname + '---' + self.authorname
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            self.patha = self.line + '\海岸线小说\{}\\'.format(self.newwname)
            if os.path.isdir(self.patha):
                pass
            else:
                os.makedirs(self.patha)
        else:
            self.patha = r'海岸线小说\{}\\'.format(self.newwname)
            if os.path.isdir(self.patha):
                pass
            else:
                os.makedirs(self.patha)
        req = '<dd><a href="(.*?)"'
        self.purl = re.findall(req, self.html)
        self.newpurl1 = []
        for i in self.purl:
            self.newpurl = 'https://www.haxds.com' + i
            self.newpurl1.append(self.newpurl)
        return self.newpurl1, self.newwname

    def download(self, url):
        header = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'www.haxds.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/48.0.2564.116 Safari/537.36',
            'Connection': 'keep-alive',
            'Referer': 'https://www.haxds.com/files/article/html/{}/index.html'.format(
                self.id)}
        html1 = requests.get(url, headers=header).text
        req = '<h1>(.*?)</h1>'
        biaoti = re.findall(req, html1)
        self.biaoti2 = biaoti[0]
        rstr = r"[\/\\\:\*\?\"\<\>\|\？]"
        self.biaoti3 = re.sub(rstr, " ", self.biaoti2)  # 替换为空格
        MYapp.text.insert(END, '正在下载章节：{}'.format(self.biaoti3))
        MYapp.text.see(END)
        MYapp.text.update()
        req1 = '<div id="BookText">(.*?)</div>'
        self.title = re.findall(req1, html1, re.S)
        return self.biaoti3, self.title

    def write(self, name, title1):
            # with open('小说下载\{}'.format(self.url_2[1]) + '\{}.txt'.format(name), 'a', encoding='utf-8') as ff:
            #     ff.write(name)
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            for i in title1:
                par = i.replace('<br /><br /> ', '')
                paragraph1 = par.replace('<br>', '\n')
                # paragraph2 = paragraph1.replace("　　", '\n')
                if os.path.exists(
                        self.line +
                        '\海岸线小说\{}'.format(
                            self.url_2[1]) +
                        '\{}.txt'.format(name)):
                    MYapp.text.insert(END, '已存在：{}'.format(name))
                    MYapp.text.see(END)
                    MYapp.text.update()
                    pass
                else:
                    with open(self.line + '\海岸线小说\{}'.format(self.url_2[1]) + '\{}.txt'.format(name), 'a',
                              encoding='utf-8') as fp:
                        # fp.write('\n')
                        fp.write(paragraph1)
                        time.sleep(0.08)
        else:
            for i in title1:
                par = i.replace('<br /><br /> ', '')
                paragraph1 = par.replace('<br>', '\n')
            # paragraph2 = paragraph1.replace("　　", '\n')

                if os.path.exists(
                        '海岸线小说\{}'.format(
                            self.url_2[1]) +
                        '\{}.txt'.format(name)):
                    MYapp.text.insert(END, '已存在：{}'.format(name))
                    MYapp.text.see(END)
                    MYapp.text.update()
                    pass
                else:
                    with open('海岸线小说\{}'.format(self.url_2[1]) + '\{}.txt'.format(name), 'a', encoding='utf-8') as fp:
                        # fp.write('\n')
                        fp.write(paragraph1)
                        time.sleep(0.08)

    def hebing(self):
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            filedir = self.line + '\海岸线小说\{}\\'.format(self.newwname)
            # 获取当前文件夹中的文件名称列表
            filenames = os.listdir(filedir)
            filenames.sort(key=lambda x: int(x[:3]))
            # 打开当前目录下的result.txt文件，如果没有则创建
            f = open(
                self.line +
                '\海岸线小说\{}.txt'.format(
                    self.newwname),
                'w',
                encoding='utf-8')
            # 先遍历文件名
            for filename in filenames:
                filepath = filedir + '/' + filename
                # 遍历单个文件，读取行数
                try:
                  for line in open(filepath, encoding='utf-8'):
                      try:
                        f.writelines(line)
                      except BaseException:
                          pass
                except BaseException:
                    pass
            f.close()
        else:
            filedir = r'海岸线小说\{}\\'.format(self.newwname)
        # 获取当前文件夹中的文件名称列表
            filenames = os.listdir(filedir)
            filenames.sort(key=lambda x: int(x[:3]))
        # 打开当前目录下的result.txt文件，如果没有则创建
            f = open(
                '海岸线小说\{}.txt'.format(
                    self.newwname),
                'w',
                encoding='utf-8')
        # 先遍历文件名
            for filename in filenames:
                filepath = filedir + '/' + filename
            # 遍历单个文件，读取行数
                try:
                  for line in open(filepath, encoding='utf-8'):
                      try:
                        f.writelines(line)
                      except BaseException:
                          pass
                except BaseException:
                    pass
            f.close()

    def stop(self):
        self.isRunning = True


class biquge(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.url1 = MYapp.entry.get()
        self.xiaoshuo_id = self.url1.split('cc/')[-1]
        self.id = self.xiaoshuo_id.replace('/', '')
        self.new_url = 'https://www.biquge5200.cc/{}/'.format(self.id)

    def run(self):
        global x
        if self.new_url == 'https://www.biquge5200.cc//':
            MYapp.text.insert(END, '请输入正确链接')
            MYapp.text.see(END)
            MYapp.text.update()
        else:
            x = 0
            self.url_2 = self.get_url(self.url1)
            for i in self.url_2[0]:
                test = self.download(i)
                c = str(x)
                a = c + '  ' + test[0]
                b = test[1]
                self.write(a, b)
                x += 1
            self.hebing()
            MYapp.text.insert(END, '合并成功')
            MYapp.text.see(END)
            MYapp.text.update()

    def get_url(self, url1):
        header = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'www.biquge5200.cc',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/48.0.2564.116 Safari/537.36',
            'Connection': 'keep-alive',
            'Referer': 'https://www.biquge5200.cc/{}/'}
        html = requests.get(url1, headers=header).text
        req1 = 'book_name" content="(.*?)"'
        book_name = re.findall(req1, html)
        req2 = 'author" content="(.*?)"'
        author_name = re.findall(req2, html)
        for a in author_name:
            self.authorname = a
        for i in book_name:
            self.newname = i
        self.newwname2 = self.newname + '---' + self.authorname
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            self.patha = self.line + '\笔趣阁小说\{}\\'.format(self.newwname2)
            if os.path.isdir(self.patha):
                pass
            else:
                os.makedirs(self.patha)
        else:
            self.patha = r'笔趣阁小说\{}\\'.format(self.newwname2)
            if os.path.isdir(self.patha):
                pass
            else:
                os.makedirs(self.patha)
        req = '<dd><a href="(.*?)"'
        self.purl = re.findall(req, html)
        return self.purl, self.newwname2

    def download(self, url):
        header = {'Accept': '*/*',
                  'Accept-Language': 'en-US,en;q=0.8',
                  'Cache-Control': 'max-age=0',
                  'Host': 'www.biquge5200.cc',
                  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/48.0.2564.116 Safari/537.36',
                  'Connection': 'keep-alive',
                  'Referer': 'https://www.biquge5200.cc/'}
        html1 = requests.get(url, headers=header).text
        req = '<h1>(.*?)</h1>'
        biaoti = re.findall(req, html1)
        self.biaoti2 = biaoti[0]
        rstr = r"[\/\\\:\*\?\"\<\>\|\？]"  # '/ \ : * ? " < > | ？'
        self.biaoti3 = re.sub(rstr, " ", self.biaoti2)  # 替换为空格
        MYapp.text.insert(END, '正在下载章节：{}'.format(self.biaoti3))
        MYapp.text.see(END)
        MYapp.text.update()
        req1 = '<div id="content">(.*?)</div>'
        self.title = re.findall(req1, html1, re.S)
        # response = request.urlopen(request.Request(url, headers=header))
        # content = response.read().decode('gbk')
        # soup = BeautifulSoup(content, 'html.parser')
        # self.title = soup.find('div', id="content").get_text()
        return self.biaoti3, self.title

    def write(self, name, title1):
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            if os.path.exists(
                    self.line +
                    '\笔趣阁小说\{}'.format(
                        self.url_2[1]) +
                    '\{}.txt'.format(name)):
                MYapp.text.insert(END, '已存在：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                pass
            else:
                with open(self.line + '\笔趣阁小说\{}'.format(self.url_2[1]) +
                          '\{}.txt'.format(name), 'a', encoding='utf-8') as ff:
                    ff.write(name + '\n')
                for i in title1:
                    par = i.replace('<p>', '')
                    paragraph1 = par.replace('</p>', '\n')
                    with open(self.line + '\笔趣阁小说\{}'.format(self.url_2[1]) + '\{}.txt'.format(name), 'a',
                              encoding='utf-8') as fp:
                        fp.write(paragraph1)
                        time.sleep(0.08)
        else:
            if os.path.exists(
                    '笔趣阁小说\{}'.format(
                        self.url_2[1]) +
                    '\{}.txt'.format(name)):
                MYapp.text.insert(END, '已存在：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                pass
            else:
                with open('笔趣阁小说\{}'.format(self.url_2[1]) + '\{}.txt'.format(name), 'a', encoding='utf-8') as ff:
                    ff.write(name + '\n')
                for i in title1:
                    par = i.replace('<p>', '')
                    paragraph1 = par.replace('</p>', '\n')
                    with open('笔趣阁小说\{}'.format(self.url_2[1]) + '\{}.txt'.format(name), 'a', encoding='utf-8') as fp:
                        fp.write(paragraph1)
                        time.sleep(0.08)

    def hebing(self):
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            filedir = self.line + \
                '\笔趣阁小说\{}\\'.format(self.newwname2)  # 获取当前文件夹中的文件名称列表
            filenames = os.listdir(filedir)  # 打开当前目录下的result.txt文件，如果没有则创建
            filenames.sort(key=lambda x: int(x[:3]))
            f = open(
                self.line +
                '\笔趣阁小说\{}.txt'.format(
                    self.newwname2),
                'w',
                encoding='utf-8')
            # 先遍历文件名
            for filename in filenames:
                filepath = filedir + '/' + filename
                # 遍历单个文件，读取行数
                try:
                  for line in open(filepath, encoding='utf-8'):
                      try:
                        f.writelines(line)
                      except BaseException:
                          pass
                except BaseException:
                    pass
            f.close()
        else:
            filedir = r'笔趣阁小说\{}\\'.format(self.newwname2)  # 获取当前文件夹中的文件名称列表
            filenames = os.listdir(filedir)  # 打开当前目录下的result.txt文件，如果没有则创建
            filenames.sort(key=lambda x: int(x[:3]))
            f = open(
                '笔趣阁小说\{}.txt'.format(
                    self.newwname2),
                'w',
                encoding='utf-8')
            # 先遍历文件名
            for filename in filenames:
                filepath = filedir + '/' + filename
                # 遍历单个文件，读取行数
                try:
                  for line in open(filepath, encoding='utf-8'):
                      try:
                        f.writelines(line)
                      except BaseException:
                          pass
                except BaseException:
                    pass
            f.close()

    def stop(self):
        self.isRunning = True


class biquge2(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.url1 = MYapp.entry.get()

    def run(self):
        self.new_url = 'https://www.biquge5200.cc' + self.newurl(self.url1)[0]
        global x
        if self.new_url == 'https://www.biquge5200.cc/':
            MYapp.text.insert(END, '请输入正确链接')
            MYapp.text.see(END)
            MYapp.text.update()
        else:
            x = 0
            self.url_2 = self.get_url(self.new_url)
            for i in self.url_2[0]:
                test = self.download(i)
                c = str(x)
                a = c + '  ' + test[0]
                b = test[1]
                self.write(a, b)
                x += 1
            self.hebing()
            MYapp.text.insert(END, '合并成功')
            MYapp.text.see(END)
            MYapp.text.update()

    @staticmethod
    def newurl(url1):
        content = url1 + ' biquge5200.cc'
        content_code = urllib.request.quote(content)
        url2 = 'https://www.baidu.com/s?wd=' + content_code
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'}
        response = requests.get(url2, headers=headers)
        response.encoding = 'utf-8'
        html2 = response.text
        link_list = re.findall(
            r'<div class.*?c-container[\s\S]*?href[\s\S]*?http://([\s\S]*?)"', html2)
        for url in link_list:
            url3 = 'http://' + url
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'}
            response = requests.get(url3, headers=headers)
            a = response.text
            req1 = 'read_url" content="(.*?)"'
            urls = re.findall(req1, a)
            req = 'www.biquge5200.cc(.*/)'
            a5 = re.findall(req, urls[0], re.S)
            if len(a5) == 0:
                pass
            else:
                return a5

    def get_url(self, url1):
        header = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/48.0.2564.116 Safari/537.36',
            'Connection': 'keep-alive',
            'Referer': 'https://www.biquge5200.cc'}
        html = requests.get(url1, headers=header).text
        req1 = 'book_name" content="(.*?)"'
        book_name = re.findall(req1, html)
        req2 = 'author" content="(.*?)"'
        author_name = re.findall(req2, html)
        for a in author_name:
            self.authorname = a
        for i in book_name:
            self.newname = i
        self.newwname2 = self.newname + '---' + self.authorname
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            self.patha = self.line + '\搜索的小说\{}\\'.format(self.newwname2)
            if os.path.isdir(self.patha):
                pass
            else:
                os.makedirs(self.patha)
        else:
            self.patha = r'搜索的小说\{}\\'.format(self.newwname2)
            if os.path.isdir(self.patha):
                pass
            else:
                os.makedirs(self.patha)
        req = '<dd><a href="(.*?)"'
        self.purl = re.findall(req, html)
        return self.purl, self.newwname2

    def download(self, url):
        header = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/48.0.2564.116 Safari/537.36',
            'Connection': 'keep-alive',
            'Referer': 'https://www.readnovel.com/'}
        html1 = requests.get(url, headers=header).text
        req = '<h1>(.*?)</h1>'
        biaoti = re.findall(req, html1)
        self.biaoti2 = biaoti[0]
        rstr = r"[\/\\\:\*\?\"\<\>\|\？]"  # '/ \ : * ? " < > | ？'
        self.biaoti3 = re.sub(rstr, " ", self.biaoti2)  # 替换为空格
        MYapp.text.insert(END, '正在下载章节：{}'.format(self.biaoti3))
        MYapp.text.see(END)
        MYapp.text.update()
        req1 = '<div id="content">(.*?)</div>'
        self.title = re.findall(req1, html1, re.S)
        return self.biaoti3, self.title

    def write(self, name, title1):
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            if os.path.exists(
                    self.line +
                    '\搜索的小说\{}'.format(
                        self.url_2[1]) +
                    '\{}.txt'.format(name)):
                MYapp.text.insert(END, '已存在：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                pass
            else:
                with open(self.line + '\搜索的小说\{}'.format(self.url_2[1]) +
                          '\{}.txt'.format(name), 'a', encoding='utf-8') as ff:
                    ff.write(name + '\n')
                for i in title1:
                    par = i.replace('<p>', '')
                    paragraph1 = par.replace('</p>', '\n')
                    with open(self.line + '\搜索的小说\{}'.format(self.url_2[1]) + '\{}.txt'.format(name), 'a',
                              encoding='utf-8') as fp:
                        fp.write(paragraph1)
                        time.sleep(0.08)
        else:
            if os.path.exists(
                    '搜索的小说\{}'.format(
                        self.url_2[1]) +
                    '\{}.txt'.format(name)):
                MYapp.text.insert(END, '已存在：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                pass
            else:
                with open('搜索的小说\{}'.format(self.url_2[1]) + '\{}.txt'.format(name), 'a', encoding='utf-8') as ff:
                    ff.write(name + '\n')
                for i in title1:
                    par = i.replace('<p>', '')
                    paragraph1 = par.replace('</p>', '\n')
                    with open('搜索的小说\{}'.format(self.url_2[1]) + '\{}.txt'.format(name), 'a', encoding='utf-8') as fp:
                        fp.write(paragraph1)
                        time.sleep(0.08)

    def hebing(self):
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            filedir = self.line + \
                '\搜索的小说\{}\\'.format(self.newwname2)  # 获取当前文件夹中的文件名称列表
            filenames = os.listdir(filedir)  # 打开当前目录下的result.txt文件，如果没有则创建
            filenames.sort(key=lambda x: int(x[:3]))
            f = open(
                self.line +
                '\搜索的小说\{}.txt'.format(
                    self.newwname2),
                'w',
                encoding='utf-8')
            # 先遍历文件名
            for filename in filenames:
                filepath = filedir + '/' + filename
                # 遍历单个文件，读取行数
                try:
                  for line in open(filepath, encoding='utf-8'):
                      try:
                        f.writelines(line)
                      except BaseException:
                          pass
                except BaseException:
                    pass
            f.close()
        else:
            filedir = r'搜索的小说\{}\\'.format(self.newwname2)  # 获取当前文件夹中的文件名称列表
            filenames = os.listdir(filedir)  # 打开当前目录下的result.txt文件，如果没有则创建
            filenames.sort(key=lambda x: int(x[:3]))
            f = open(
                '搜索的小说\{}.txt'.format(
                    self.newwname2),
                'w',
                encoding='utf-8')
            # 先遍历文件名
            for filename in filenames:
                filepath = filedir + '/' + filename
                # 遍历单个文件，读取行数
                try:
                  for line in open(filepath, encoding='utf-8'):
                      try:
                        f.writelines(line)
                      except BaseException:
                          pass
                except BaseException:
                    pass
            f.close()

    def stop(self):
        self.isRunning = True


class find(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.url1 = MYapp.entry.get()

    def run(self):
        self.search_book(self.url1)

    def search_book(self, bookname):
        header = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/48.0.2564.116 Safari/537.36',
            'Connection': 'keep-alive',
            'Referer': 'https://www.biquge5200.cc'}
        url = 'http://www.biquge5200.com/modules/article/search.php?searchkey=' + \
            parse.quote(bookname)
        # response = request.urlopen(url)
        # content = response.read().decode('gbk')
        response = requests.get(url, headers=header)
        content=response.text
        soup = BeautifulSoup(content, 'html.parser')
        self.key = 1
        path = r'{}result.txt'.format(bookname)
        if os.path.exists(path):
            for row in soup.find('table').find_all('tr'):
                td1 = row.select('td:nth-of-type(1)')
                td3 = row.select('td:nth-of-type(3)')
                if (td1 and td3):
                    name = td1[0].find('a').string
                    author = td3[0].string
                    MYapp.text.insert(END, str(self.key) +
                                      ' 书名：' + name + ' >> 作者：' + author)
                    MYapp.text.see(END)
                    MYapp.text.update()
                    self.key += 1
        else:
            for row in soup.find('table').find_all('tr'):
                td1 = row.select('td:nth-of-type(1)')
                td3 = row.select('td:nth-of-type(3)')
                if (td1 and td3):
                    name = td1[0].find('a').string
                    href = td1[0].find('a').get('href')
                    author = td3[0].string
                    MYapp.text.insert(END, str(self.key) +
                                      ' 书名：' + name + ' >> 作者：' + author)
                    MYapp.text.see(END)
                    MYapp.text.update()
                    self.key += 1

                    with open('{}result.txt'.format(bookname), 'a', encoding='utf-8') as fp:
                        fp.write(name + ' ' + href + '\n')

    def stop(self):
        self.isRunning = True


class input(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.line = Select.entry.get()

    def run(self):
        self.line2 = int(self.line)
        test = find()
        filename = '{}result.txt'.format(test.url1)
        count = linecache.getline(filename, self.line2)
        req = 'www.biquge5200.cc(.*/)'
        a5 = re.findall(req, count, re.S)
        self.real_url = 'https://www.biquge5200.cc' + a5[0]
        global x
        if self.real_url == 'https://www.biquge5200.cc/':
            MYapp.text.insert(END, '请输入正确链接')
            MYapp.text.see(END)
            MYapp.text.update()
        else:
            x = 0
            self.url_2 = self.get_url(self.real_url)
            for i in self.url_2[0]:
                test = self.download(i)
                c = str(x)
                # d=int(test[0])
                a = c + '  ' + test[0]
                b = test[1]
                self.write(a, b)
                x += 1
            self.hebing()
            MYapp.text.insert(END, '合并成功')
            MYapp.text.see(END)
            MYapp.text.update()

    @staticmethod
    def newurl(url1):
        content = url1 + ' biquge5200.cc'
        content_code = urllib.request.quote(content)
        url2 = 'https://www.baidu.com/s?wd=' + content_code
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'}
        response = requests.get(url2, headers=headers)
        response.encoding = 'utf-8'
        html2 = response.text
        link_list = re.findall(
            r'<div class.*?c-container[\s\S]*?href[\s\S]*?http://([\s\S]*?)"', html2)
        for url in link_list:
            url3 = 'http://' + url
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                'AppleWebKit/537.36 (KHTML, like Gecko) '
                'Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'}
            response = requests.get(url3, headers=headers)
            a = response.text
            req1 = 'read_url" content="(.*?)"'
            urls = re.findall(req1, a)
            req = 'www.biquge5200.cc(.*/)'
            a5 = re.findall(req, urls[0], re.S)
            if len(a5) == 0:
                pass
            else:
                return a5

    def get_url(self, url1):
        header = {'Accept': '*/*',
                  'Accept-Language': 'en-US,en;q=0.8',
                  'Cache-Control': 'max-age=0',
                  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/48.0.2564.116 Safari/537.36',
                  'Connection': 'keep-alive',
                  'Referer': 'https://www.biquge5200.cc'}
        html = requests.get(url1, headers=header).text
        req1 = 'book_name" content="(.*?)"'
        book_name = re.findall(req1, html)
        req2 = 'author" content="(.*?)"'
        author_name = re.findall(req2, html)
        for a in author_name:
            self.authorname = a
        for i in book_name:
            self.newname = i
        self.newwname2 = self.newname + '---' + self.authorname
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            self.patha = self.line + '\搜索的小说\{}\\'.format(self.newwname2)
            if os.path.isdir(self.patha):
                pass
            else:
                os.makedirs(self.patha)
        else:
            self.patha = r'搜索的小说\{}\\'.format(self.newwname2)
            if os.path.isdir(self.patha):
                pass
            else:
                os.makedirs(self.patha)
        req = '<dd><a href="(.*?)"'
        self.purl = re.findall(req, html)
        return self.purl, self.newwname2

    def download(self, url):
        header = {'Accept': '*/*',
                  'Accept-Language': 'en-US,en;q=0.8',
                  'Cache-Control': 'max-age=0',
                  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/48.0.2564.116 Safari/537.36',
                  'Connection': 'keep-alive',
                  'Referer': 'https://www.readnovel.com/'}
        html1 = requests.get(url, headers=header).text
        req = '<h1>(.*?)</h1>'
        biaoti = re.findall(req, html1)
        self.biaoti2 = biaoti[0]
        rstr = r"[\/\\\:\*\?\"\<\>\|\？]"  # '/ \ : * ? " < > | ？'
        self.biaoti3 = re.sub(rstr, " ", self.biaoti2)  # 替换为空格
        MYapp.text.insert(END, '正在下载章节：{}'.format(self.biaoti3))
        MYapp.text.see(END)
        MYapp.text.update()
        req1 = '<div id="content">(.*?)</div>'
        self.title = re.findall(req1, html1, re.S)
        return self.biaoti3, self.title

    def write(self, name, title1):
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            if os.path.exists(
                    self.line +
                    '\搜索的小说\{}'.format(
                        self.url_2[1]) +
                    '\{}.txt'.format(name)):
                MYapp.text.insert(END, '已存在：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                pass
            else:
                with open(self.line + '\搜索的小说\{}'.format(self.url_2[1]) + '\{}.txt'.format(name), 'a',
                          encoding='utf-8') as ff:
                    ff.write(name + '\n')
                for i in title1:
                    par = i.replace('<p>', '')
                    paragraph1 = par.replace('</p>', '\n')
                    with open(self.line + '\搜索的小说\{}'.format(self.url_2[1]) + '\{}.txt'.format(name), 'a',
                              encoding='utf-8') as fp:
                        fp.write(paragraph1)
                        time.sleep(0.08)
        else:
            if os.path.exists(
                    '搜索的小说\{}'.format(
                        self.url_2[1]) +
                    '\{}.txt'.format(name)):
                MYapp.text.insert(END, '已存在：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                pass
            else:
                with open('搜索的小说\{}'.format(self.url_2[1]) + '\{}.txt'.format(name), 'a', encoding='utf-8') as ff:
                    ff.write(name + '\n')
                for i in title1:
                    par = i.replace('<p>', '')
                    paragraph1 = par.replace('</p>', '\n')
                    with open('搜索的小说\{}'.format(self.url_2[1]) + '\{}.txt'.format(name), 'a', encoding='utf-8') as fp:
                        fp.write(paragraph1)
                        time.sleep(0.08)

    def hebing(self):
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            filedir = self.line + \
                '\搜索的小说\{}\\'.format(self.newwname2)  # 获取当前文件夹中的文件名称列表
            filenames = os.listdir(filedir)  # 打开当前目录下的result.txt文件，如果没有则创建
            filenames.sort(key=lambda x: int(x[:3]))
            f = open(
                self.line +
                '\搜索的小说\{}.txt'.format(
                    self.newwname2),
                'w',
                encoding='utf-8')
            # 先遍历文件名
            for filename in filenames:
                filepath = filedir + '/' + filename
                # 遍历单个文件，读取行数
                try:
                  for line in open(filepath, encoding='utf-8'):
                      try:
                        f.writelines(line)
                      except BaseException:
                          pass
                except BaseException:
                    pass
            f.close()
        else:
            filedir = r'搜索的小说\{}\\'.format(self.newwname2)  # 获取当前文件夹中的文件名称列表

            filenames = os.listdir(filedir)  # 打开当前目录下的result.txt文件，如果没有则创建
            filenames.sort(key=lambda x: int(x[:3]))
            f = open(
                '搜索的小说\{}.txt'.format(
                    self.newwname2),
                'w',
                encoding='utf-8')
            # 先遍历文件名
            for filename in filenames:
                filepath = filedir + '/' + filename
                # 遍历单个文件，读取行数
                try:
                  for line in open(filepath, encoding='utf-8'):
                      try:
                        f.writelines(line)
                      except BaseException:
                          pass
                except BaseException:
                    pass
            f.close()

    def stop(self):
        self.isRunning = True


def download():
    test = haianxian()
    test.start()


def download2():
    test = biquge()
    test.start()


def download3():
    test = find()
    test.start()


def download4():
    test = input()
    test.start()


if __name__ == '__main__':
    app = MYapp()
    section = section()
    menu = Menu(app, tearoff=0)
    menu.add_command(label="复制", command=section.oncopy)
    menu.add_separator()
    menu.add_command(label="粘贴", command=section.onpaste)
    menu.add_separator()
    menu.add_command(label="剪切", command=section.oncut)

    def popupmenu(event):
        menu.post(event.x_root, event.y_root)

    MYapp.entry.bind("<Button-3>", popupmenu)
    app.mainloop()
