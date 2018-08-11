#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time   : 2018/7/29 0029 20:25
# @Author : wangyulin
# @File   : 爬取小说.py
#单线程稳定版
import requests
import win32con, win32api
import wx
import linecache
import time
from flashtext import KeywordProcessor
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
                '微软雅黑', 14), command=download2)
        button.place(x=5, y=316.5, width=110, height=45)
        button = Button(
            self, text='海岸线小说', font=(
                '微软雅黑', 14), command=download)
        button.place(x=125, y=316.5, width=110, height=45)
        button = Button(
            self, text='搜索小说', font=(
                '微软雅黑', 14), command=download3)
        button.place(x=125, y=365, width=110, height=45)
        button = Button(
            self, text='奇书网\n(直接下载)', font=('微软雅黑', 13), command=download5)
        button.place(x=239, y=316.5, width=110, height=45)
        fu = local()
        button = Button(
            self, text='指定路径', font=(
                '微软雅黑', 14), command=fu.lujing)
        button.place(x=352, y=316.5, width=90, height=45)
        button = Button(
            self, text='开始下载', font=(
                '微软雅黑', 14), command=self.top)
        button.place(x=352, y=365, width=90, height=45)
        button = Button(
            self, text='清空地址栏', font=(
                '微软雅黑', 14), command=self.qingkong)
        button.place(x=5, y=365, width=110, height=45)
        button = Button(
            self, text='退出程序', font=(
                '微软雅黑', 14), command=self.destroy)
        button.place(x=452, y=365, width=90, height=45)
        button = Button(
            self, text='打开文件', font=(
                '微软雅黑', 14), command=self.dakai)
        button.place(x=452, y=316.5, width=90, height=45)

    def top(self):
        global top
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
        # top.destroy()

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
                win32api.SetFileAttributes('log.txt', win32con.FILE_ATTRIBUTE_HIDDEN)
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
        start=time.time()
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
        end=time.time()
        print('%d'%(end-start))
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
            'Referer': url}
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
                    MYapp.text.insert(END, "%s存在问题" % filename)
                    MYapp.text.see(END)
                    MYapp.text.update()
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
                    MYapp.text.insert(END, "%s存在问题" % filename)
                    MYapp.text.see(END)
                    MYapp.text.update()
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
        # soup = BeautifulSoup(html1, 'html.parser')
        # biaoti=soup.find_all('h1')
        # for i in biaoti:
            # print(i)
        # print(biaoti)
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
                    # flashtext  用法
                    # start=time.time()
                    # ke = KeywordProcessor()
                    # ke.add_keyword('<p>　　', ' ')
                    # title = ke.replace_keywords(i)
                    # kp=KeywordProcessor()
                    # kp.add_keyword('</p>','\n')
                    # paragraph1=kp.replace_keywords(title)
                    # end=time.time()
                    # print('time1',end-start)
                    start2 = time.time()
                    par = i.replace('<p>', '')
                    paragraph1 = par.replace('</p>', '\n')
                    end2 = time.time()
                    print('time2',end2-start2)
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
                    MYapp.text.insert(END, "%s存在问题" % filename)
                    MYapp.text.see(END)
                    MYapp.text.update()
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
                    MYapp.text.insert(END, "%s存在问题" % filename)
                    MYapp.text.see(END)
                    MYapp.text.update()
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
                    MYapp.text.insert(END, "%s存在问题" % filename)
                    MYapp.text.see(END)
                    MYapp.text.update()
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
                    MYapp.text.insert(END, "%s存在问题" % filename)
                    MYapp.text.see(END)
                    MYapp.text.update()
            f.close()

    def stop(self):
        self.isRunning = True
class qishuwang(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.url1 = MYapp.entry.get()

    def run(self):
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            self.patha = self.line + '\奇书网小说\\'
            if os.path.isdir(self.patha):
                pass
            else:
                os.makedirs(self.patha)
        else:
            self.patha = r'奇书网小说\\'
            if os.path.isdir(self.patha):
                pass
            else:
                os.makedirs(self.patha)
        if self.url1 == '':
            MYapp.text.insert(END, "请输入小说完整名字")
            MYapp.text.see(END)
            MYapp.text.update()
        else:
            self.search_book(self.url1)
            MYapp.text.insert(END, "下载完毕")
            MYapp.text.see(END)
            MYapp.text.update()

    def search_book(self, bookname):
        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'xiazai.xqishu.com',
            'If-Modified-Since': 'Thu, 11 Jan 2018 10:46: 24GMT',
            'If-None-Match': "6b8be66cc98ad31:116b",
            'Upgrade-Insecure-Requests': '1',
            'Referer': 'http://www.qishu.cc/txt/65014.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) '
            'Gecko/20100101 Firefox/61.0'}
        url3 = 'http://dl.kusuu.net/rar/' + parse.quote(bookname) + '.rar'
        # url4='https://dz.80txt.com/75964/' + parse.quote(bookname) + '.zip'搜索无效等待解决
        # urllib.request.urlretrieve(url4, self.line + '\奇书网小说\{}.zip'.format(bookname))
        url2 = 'http://xiazai.xqishu.com/txt/' + parse.quote(bookname) + '.txt'
        # url='http://down.xqishu.com/txt/%E6%81%8B%E9%93%B6%E8%89%B2%E7%9A%84%E6%98%9F%E9%99%85.txt'
        url1 = 'http://down.xqishu.com/txt/' + parse.quote(bookname) + '.txt'
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
                try:
                    # socket.setdefaulttimeout(20)
                    MYapp.text.insert(END, '正在下载小说：{}.rar'.format(bookname))
                    MYapp.text.see(END)
                    MYapp.text.update()
                    urllib.request.urlretrieve(
                        url3, self.line + '\奇书网小说\{}.rar'.format(bookname))
                except BaseException as e:
                    MYapp.text.insert(END, "未找到，正在尝试搜寻其他源")
                    MYapp.text.see(END)
                    MYapp.text.update()
                    try:
                        MYapp.text.insert(
                            END, '正在下载小说：{}.txt--速度较慢'.format(bookname))
                        MYapp.text.see(END)
                        MYapp.text.update()
                        urllib.request.u
                    except BaseException:
                        MYapp.text.insert(END, "对不起，找到此小说")
                        MYapp.text.see(END)
                        MYapp.text.update()
        else:

                # r=requests.get(url2,headers=header)
                # a=request.urlopen(url1)
                # response1 = urllib.request.Request(url3,data=None,headers=header)
                # response=urllib.request.urlopen(response1)
                # responseCode = response.getcode()
                # a=response.read().decode("gbk")
                # print(response)
                # r2 = requests.get(a, headers=header)
                #  r2.raise_for_status()
                #  playFile = open('RomeoAndJuliet.txt', 'wb')
                #  for chunk in r2.iter_content(100000):
                #      playFile.write(chunk)
                # with open('奇书网小说\{}.txt'.format(bookname), "wb") as code:
                #     code.write(a.content)
            try:
                    # socket.setdefaulttimeout(20)
                MYapp.text.insert(END, '正在下载小说：{}.rar'.format(bookname))
                MYapp.text.see(END)
                MYapp.text.update()
                urllib.request.urlretrieve(
                    url3, '奇书网小说\{}.rar'.format(bookname))

            except BaseException as e:
                MYapp.text.insert(END, "未找到，正在尝试搜寻其他源")
                MYapp.text.see(END)
                MYapp.text.update()
                try:
                    MYapp.text.insert(
                        END, '正在下载小说：{}.txt--速度较慢'.format(bookname))
                    MYapp.text.see(END)
                    MYapp.text.update()
                    urllib.request.urlretrieve(
                        url1, '奇书网小说\{}.txt'.format(bookname))
                    try:
                        urllib.request.urlretrieve(url2, '奇书网小说\{}.txt'.format(bookname))
                    except BaseException:
                        pass
                except BaseException:
                    MYapp.text.insert(END, "对不起，找到此小说")
                    MYapp.text.see(END)
                    MYapp.text.update()

    def stop(self):
        self.isRunning = True

class find(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.url1 = MYapp.entry.get()
        if self.url1=='':
            MYapp.text.insert(END,'请输入小说名称')
            MYapp.text.see(END)
            MYapp.text.update()
        else:
            self.pathg=r'search_log\\'

            if os.path.isdir(self.pathg):
                 pass
            else:
                os.makedirs(self.pathg)
                win32api.SetFileAttributes('search_log', win32con.FILE_ATTRIBUTE_HIDDEN)
            with open('search_log\\resultlog.txt', 'w', encoding='utf-8') as f:
                f.write(self.url1)
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
        self.pathh=r'book_log\\'

        if os.path.isdir(self.pathh):
            pass
        else:
            os.makedirs(self.pathh)
            win32api.SetFileAttributes('book_log', win32con.FILE_ATTRIBUTE_HIDDEN)
        path = r'book_log\{}result.txt'.format(bookname)
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

                    with open('book_log\{}result.txt'.format(bookname), 'a', encoding='utf-8') as fp:
                        fp.write(name + ' ' + href + '\n')

    def stop(self):
        self.isRunning = True


class input(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.line = Select.entry.get()
        top.destroy()
    def run(self):
        self.line2 = int(self.line)
        path3=r'search_log\resultlog.txt'
        count2 = linecache.getline(path3, 1)
        count3=count2.replace('\n','')
        filename = 'book_log\{}result.txt'.format(count3)
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
                    MYapp.text.insert(END, "%s存在问题" % filename)
                    MYapp.text.see(END)
                    MYapp.text.update()
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
                    MYapp.text.insert(END, "%s存在问题" % filename)
                    MYapp.text.see(END)
                    MYapp.text.update()
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
def download5():
    test = qishuwang()
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
