#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time   : 2018/7/29 0029 20:25
# @Author : wangyulin
# @File   : 爬取小说.py
import requests
import win32con
# import socket
from time import sleep, ctime
# import queue
import urllib3
from lxml import etree
import win32api
import linecache
# from threading import Thread
import time
# import multiprocessing
# from multiprocessing import Pool
from multiprocessing.dummy import Pool
# from multiprocessing.dummy import
# from flashtext import KeywordProcessor
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
urllib3.disable_warnings()


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
        path2 = r'log.txt'  # 读取路径记录文件
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
        lable.place(x=0, y=2, width=260, height=35)
        MYapp.url = StringVar()  # 这即是输入框中的内容
        MYapp.entry = Entry(
            self, textvariable=MYapp.url, font=(
                '微软雅黑', 15))
        MYapp.entry.place(x=260, y=2, width=220, height=35)
        button = Button(
            self, text='清空', font=(
                '微软雅黑', 14), command=self.qingkong)
        button.place(x=482, y=2, width=60, height=35)
        MYapp.text = Listbox(self, font=('微软雅黑', 15))
        MYapp.text.place(x=0, y=40, width=550, height=275)
        # scr1 = Scrollbar(self)
        # MYapp.text.configure(yscrollcommand=scr1.set)
        # scr1['command'] = MYapp.text.yview
        # scr1.place(x=482, y=2, width=10, height=60)

        button = Button(
            self, text='笔趣阁小说', font=(
                '微软雅黑', 14), command=download2)
        button.place(x=5, y=316.5, width=110, height=45)
        button = Button(
            self, text='海岸线小说', font=(
                '微软雅黑', 14), command=download)
        button.place(x=122, y=316.5, width=110, height=45)
        button = Button(
            self, text='全本网搜索\n(速度快)', font=(
                '微软雅黑', 13), command=download3)
        button.place(x=122, y=365, width=110, height=45)
        button = Button(
            self, text='奇书网\n(直接下载)', font=('微软雅黑', 13), command=download5)
        button.place(x=239, y=316.5, width=110, height=45)
        button = Button(
            self, text='顶点网搜索\n'
            '(速度快)', font=(
                '微软雅黑', 13), command=download6)
        button.place(x=239, y=365, width=110, height=45)
        fu = local()
        button = Button(
            self, text='指定路径', font=(
                '微软雅黑', 14), command=fu.lujing)
        button.place(x=354, y=316.5, width=90, height=45)
        button = Button(
            self, text='开始下载', font=(
                '微软雅黑', 14), command=self.top)
        button.place(x=354, y=365, width=90, height=45)
        button = Button(
            self, text='5200全本\n小说(4线程)', font=(
                '微软雅黑', 13), command=download7)
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
        powx = (sw - ww) / 2
        powy = (sh - wh) / 2
        # self.iconbitmap('icons\\format.ico')
        # 图标
        top.geometry("%dx%d+%d+%d" % (ww, wh, powx, powy))
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
        Select.url3 = StringVar()  # top界面下的 输入框
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
                win32api.SetFileAttributes(
                    'log.txt', win32con.FILE_ATTRIBUTE_HIDDEN)
                fp.write(local.path_)

        else:
            pass


class Select(Tk):
    # top界面下的输入框
    def __init__(self):
        super().__init__()
        self.setup()

    def setup(self):
        Select.url3 = StringVar()
        Select.entry = Entry(
            self, textvariable=Select.url3, font=(
                '微软雅黑', 15))
        Select.entry.grid(row=0, column=1)

# 海岸线小说  https://www.haxwx11.com


class haianxian(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.url1 = MYapp.entry.get()
        self.xiaoshuo_id = self.url1.split('info/')[-1]

        if self.xiaoshuo_id == self.url1:
            try:
                self.newwurl = self.xiaoshuo_id.split('/files/')[-2]
                self.host = self.newwurl.split('//')[1]
                self.new_url = self.xiaoshuo_id
            except IndexError:
                MYapp.text.insert(END, "请输入正确网址")
                MYapp.text.see(END)
                MYapp.text.update()
        else:
            self.id = self.xiaoshuo_id.replace('.htm', '')
            self.newwurl = self.url1.split('/files/')[-2]
            # https://www.haxwx11.com/files/article/info/0/67.htm
            # https://www.haxwx11.com/files/article/html/0/67/index.html
            self.new_url = self.newwurl + \
                '/files/article/html/{}/index.html'.format(self.id)
            self.host = self.newwurl.split('//')[1]

    def xiaoshuo(self, url):
        url2 = url['name']
        try:
            header = {
                'Accept': '*/*',
                'Accept-Language': 'en-US,en;q=0.8',
                'Cache-Control': 'max-age=0',
                'Host': self.host,
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                              'AppleWebKit/537.36 (KHTML, like Gecko) '
                              'Chrome/48.0.2564.116 Safari/537.36',
                'Connection': 'keep-alive',
                'Referer': url2}
            html1 = requests.get(url2, headers=header, timeout=35).text
            req = '<h1>(.*?)</h1>'
            biaoti = re.findall(req, html1)
            self.biaoti2 = biaoti[0]
            rstr = r"[\/\\\:\*\?\"\<\>\|\？]"
            self.biaoti3 = re.sub(rstr, " ", self.biaoti2)  # 替换为空格
            req1 = '<div id="BookText">(.*?)</div>'
            self.title = re.findall(req1, html1, re.S)
            self.zhangjie_id = url2.split('/')[8]
            self.zhangjie = self.zhangjie_id.replace('.html', '')
            for i in self.title:
                par = i.replace('<br /><br /> \n', '')
                self.paragraph1 = par.replace(
                    '<br><br>', '\n', 1).replace('<br><br>  ', '\n').replace(
                    '    全文字小说-www.', '')
                # paragraph2 = paragraph1.replace("　　", '\n')
            self.write(self.biaoti3, self.paragraph1, self.zhangjie)
        except BaseException:
            pass

    def run(self):
        start = time.time()
        global x
        try:
            self.new_url3 = self.new_url.split('html')[0]
        except AttributeError:
            return
        if self.new_url3 != self.newwurl + '/files/article/':
            MYapp.text.insert(END, '请输入正确地址')
            MYapp.text.see(END)
            MYapp.text.update()
        else:
            self.url_2 = self.get_url(self.new_url)
            self.url_3 = self.url_2[0]
            pool = Pool(processes=35)  # 创建10个进程
            pool.map(self.xiaoshuo, [self.url_3[each] for each in self.url_3])
            pool.close()
            pool.join()
            self.hebing()
            MYapp.text.insert(END, '合并成功')
            MYapp.text.see(END)
            MYapp.text.update()
            end = time.time()
            MYapp.text.insert(END, '耗费时间：%d s' % (end - start))
            MYapp.text.see(END)
            MYapp.text.update()

    def get_url(self, url1):
        header = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            # 'Host': 'www.haxds11.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) '
            'Chrome/48.0.2564.116 Safari/537.36',
            'Connection': 'keep-alive',
            # 'Referer': url1
        }
        try:
            # proxies = {"http": "36.99.17.52", },proxies=proxies
            # requests.get("http://example.org", proxies=proxies)
            self.html = requests.get(url1, headers=header, timeout=35).text
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
            chapter_all_dict = {}
            for i in self.purl:
                self.newpurl = self.newwurl + i
                self.newpurl1.append(self.newpurl)
            global x
            x = 0
            for each in self.newpurl1:
                chapter_each = {}
                chapter_each['name'] = each  # 获取章节名字
                chapter_num = int(x)  # 提取章节序号
                chapter_all_dict[chapter_num] = chapter_each  # 记录到所有的章节的字典中保存
                x += 1
            return chapter_all_dict, self.newwname
        except BaseException:
            pass

    def write(self, name, title1, zhangjie_xuhao):
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            if os.path.exists(
                self.line +
                '\海岸线小说\{}'.format(
                    self.url_2[1]) +
                '\{}'.format(zhangjie_xuhao) +
                ' ' +
                    '{}.txt'.format(name)):
                MYapp.text.insert(END, '已存在：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                pass
            else:
                MYapp.text.insert(END, '正在下载：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                with open(self.line + '\海岸线小说\{}'.format(self.url_2[1]) + '\{}'.format(zhangjie_xuhao) + ' ' + '{}.txt'.format(name), 'a',
                          encoding='utf-8') as fp:
                    fp.write(title1)
                    time.sleep(0.08)
        else:
            if os.path.exists(
                '海岸线小说\{}'.format(
                    self.url_2[1]) +
                '\{}'.format(zhangjie_xuhao) +
                ' ' +
                    '{}.txt'.format(name)):

                MYapp.text.insert(END, '已存在：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                pass
            else:
                MYapp.text.insert(END, '正在下载：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                with open('海岸线小说\{}'.format(self.url_2[1]) + '\{}'.format(zhangjie_xuhao) + ' ' + '{}.txt'.format(name), 'a', encoding='utf-8') as fp:

                    fp.write(title1)
                    time.sleep(0.08)

    def hebing(self):
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            filedir = self.line + '\海岸线小说\{}\\'.format(self.newwname)
            # 获取当前文件夹中的文件名称列表
            filenames = os.listdir(filedir)
            filenames.sort(key=lambda powx: int(powx[:-1].split()[0]))
            # 打开当前目录下的result.txt文件，如果没有则创建 1
            with open(
                self.line +
                '\海岸线小说\{}.txt'.format(
                    self.newwname),
                'w',
                    encoding='utf-8') as f:

                for filename in filenames:  # 先遍历文件名
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

        else:
            filedir = r'海岸线小说\{}\\'.format(self.newwname)
        # 获取当前文件夹中的文件名称列表
            filenames = os.listdir(filedir)
            filenames.sort(key=lambda powx: int(powx[:-1].split()[0]))
        # 打开当前目录下的result.txt文件，如果没有则创建
            with open(
                '海岸线小说\{}.txt'.format(
                    self.newwname),
                'w',
                    encoding='utf-8') as f:
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

    def stop(self):
        self.isRunning = True

# 笔趣阁小说  https://www.biquge5200.cc


class biquge(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.url1 = MYapp.entry.get()
        self.xiaoshuo_id = self.url1.split('cc/')[-1]
        self.id = self.xiaoshuo_id.replace('/', '')
        self.new_url = 'https://www.biquge5200.cc/{}/'.format(self.id)

    def get_content(self, html):
        self.urls1 = []
        self.urls1.append(html)
        for i in self.urls1:
            pool = Pool(4)
            # 使用map进行并行爬取，save_content为爬取保存函数，
            # urls为一个list,里面存储的为网址列表和对应的保存名字
            pool.map_async(self.xiaoshuo, i)
            pool.close()
            pool.join()

    def xiaoshuo(self, url):
        test = self.download(url)
        a = test[0]
        b = test[1]
        d = test[2]
        self.write(a, b, d)
        time.sleep(1.5)

    def run(self):
        global x
        if self.new_url == 'https://www.biquge5200.cc//':

            MYapp.text.insert(END, '请输入正确链接')
            MYapp.text.see(END)
            MYapp.text.update()
        else:
            # x = 1
            self.url_2 = self.get_url(self.url1)
            try:
                self.get_content(self.url_2[0])
                self.hebing()
                MYapp.text.insert(END, '合并成功')
                MYapp.text.see(END)
                MYapp.text.update()
            except TypeError:
                MYapp.text.insert(END, '请输入正确链接')
                MYapp.text.see(END)
                MYapp.text.update()

    def get_url(self, url1):

        header = {
            'Accept': 'text/css,*/*;q=0.1',
            'Accept-Encoding': 'gzip,deflate,br',
            'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Cache-Control': 'no-transform',
            'Host': 'www.biquge5200.cc',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; '
                          'x64; rv:63.0) Gecko/20100101 '
                          'Firefox/63.0',
            'Connection': 'keep-alive',
            'Referer': url1}
        try:
            html = requests.get(url1, headers=header, timeout=35).text
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
        except BaseException:
            pass

    def download(self, url):
        header = {'Accept': '*/*',
                  'Accept-Language': 'en-US,en;q=0.8',
                  'Cache-Control': 'max-age=0',
                  'Host': 'www.biquge5200.cc',
                  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/48.0.2564.116 Safari/537.36',
                  'Connection': 'keep-alive',
                  'Referer': url}
        try:
            html1 = requests.get(url, headers=header, timeout=35).text
            self.zhangjie_id = url.split('/')[4]
            self.zhangjie = self.zhangjie_id.replace('.html', '')
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
            return self.biaoti3, self.title, self.zhangjie
        except BaseException:
            pass

    def write(self, name, title1, zhangjie_xuhao):
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            if os.path.exists(
                self.line +
                '\笔趣阁小说\{}'.format(
                    self.url_2[1]) +
                '\{}'.format(zhangjie_xuhao) +
                ' ' +
                    '{}.txt'.format(name)):
                MYapp.text.insert(END, '已存在：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                pass
            else:
                with open(self.line + '\笔趣阁小说\{}'.format(self.url_2[1]) +
                          '\{}'.format(zhangjie_xuhao) + ' ' + '{}.txt'.format(name), 'a', encoding='utf-8') as ff:
                    ff.write(name + '\n')
                for i in title1:
                    par = i.replace('<p>', '')
                    paragraph1 = par.replace('</p>', '\n')
                    with open(self.line + '\笔趣阁小说\{}'.format(self.url_2[1]) + '\{}'.format(zhangjie_xuhao) + ' ' + '{}.txt'.format(name), 'a',
                              encoding='utf-8') as fp:
                        fp.write(paragraph1)
                        time.sleep(0.08)
        else:
            if os.path.exists(
                '笔趣阁小说\{}'.format(
                    self.url_2[1]) +
                '\{}'.format(zhangjie_xuhao) +
                ' ' +
                    '{}.txt'.format(name)):
                MYapp.text.insert(END, '已存在：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                pass
            else:
                with open('笔趣阁小说\{}'.format(self.url_2[1]) + '\{}'.format(zhangjie_xuhao) + ' ' + '{}.txt'.format(name), 'a', encoding='utf-8') as ff:
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
                    par = i.replace('<p>', '')
                    paragraph1 = par.replace('</p>', '\n')
                    with open('笔趣阁小说\{}'.format(self.url_2[1]) + '\{}'.format(zhangjie_xuhao) + ' ' + '{}.txt'.format(name), 'a', encoding='utf-8') as fp:
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
            # filenames.sort(key=lambda powx: int(powx[:-1].split()[0]))
            with open(
                self.line +
                '\笔趣阁小说\{}.txt'.format(
                    self.newwname2),
                'w',
                    encoding='utf-8') as f:
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

        else:
            filedir = r'笔趣阁小说\{}\\'.format(self.newwname2)  # 获取当前文件夹中的文件名称列表
            filenames = os.listdir(filedir)  # 打开当前目录下的result.txt文件，如果没有则创建
            # filenames.sort(key=lambda powx: int(powx[:-1].split()[0]))

            with open(
                '笔趣阁小说\{}.txt'.format(
                    self.newwname2),
                'w',
                    encoding='utf-8') as f:
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

    def stop(self):
        self.isRunning = True


class quanbenyuedu(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.url1 = MYapp.entry.get()
        if self.url1 == '':
            pass
        else:
            self.pathg = r'search_log\\'

            if os.path.isdir(self.pathg):
                pass
            else:
                os.makedirs(self.pathg)
                win32api.SetFileAttributes(
                    'search_log', win32con.FILE_ATTRIBUTE_HIDDEN)
                # win32api.SetFileAttributes('search_log', win32con.FILE_ATTRIBUTE_READONLY)
            with open('search_log\\resultlog.txt', 'w', encoding='utf-8') as f:
                f.write('quanbenyuedu ' + self.url1)

    def run(self):
        if self.url1 == '':
            MYapp.text.insert(END, '请输入小说名称')
            MYapp.text.see(END)
            MYapp.text.update()
            return
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

            'Referer': 'http://www.quanwenyuedu.io'}
        url = 'http://www.quanwenyuedu.io/index.php?c=xs&a=search&keywords=' + \
            parse.quote(bookname)
        try:
            response = requests.get(url, headers=header, timeout=35)
            content = response.text
        except requests.exceptions.ConnectionError:
            MYapp.text.insert(END, "请检查网络连接")
            MYapp.text.see(END)
            MYapp.text.update()
            return
        req5 = '</span><span>(.*?)</span><span>'
        page = re.findall(req5, content)[0]
        self.aa = page.split('/ ')[1]
        self.page_num = int(self.aa)
        if self.page_num == 1:
            req = '<h3><a href="(.*?)">.*?</a></h3>'
            xiaoshuo_id = re.findall(req, content)
            req1 = '<h3><a href=".*?">(.*?)</a></h3>'
            book_name = re.findall(req1, content)
            req2 = '<p>.*?<span>(.*?)</span></p>'
            author_name = re.findall(req2, content)
            self.new_url = []
            chapter_all_dict = {}
            for i in xiaoshuo_id:
                self.newurl = 'http://www.quanwenyuedu.io' + i
                self.new_url.append(self.newurl)

            global x
            x = 0
            for each in self.new_url:
                chapter_each = {}
                chapter_each['book_url'] = each  # 获取书本url
                chapter_each['book_author'] = book_name[x] + \
                    '--->' + author_name[x]
                chapter_num = int(x)  # 书本序号
                chapter_all_dict[chapter_num] = chapter_each  # 记录到所有的章节的字典中保存
                x += 1
            self.pathh = r'book_log\\'
            if os.path.isdir(self.pathh):
                pass
            else:
                os.makedirs(self.pathh)
                win32api.SetFileAttributes(
                    'book_log', win32con.FILE_ATTRIBUTE_HIDDEN)
            path = r'book_log\{}result.txt'.format(bookname)
            if os.path.exists(path):
                global b
                b = 1
                for each in chapter_all_dict:
                    each_one = chapter_all_dict[each]
                    MYapp.text.insert(
                        END, str(b) + '  ' + each_one['book_author'])
                    MYapp.text.see(END)
                    MYapp.text.update()
                    b += 1
            else:
                global a
                a = 1
                for each in chapter_all_dict:
                    each_one = chapter_all_dict[each]
                    MYapp.text.insert(
                        END, str(a) + '  ' + each_one['book_author'])
                    MYapp.text.see(END)
                    MYapp.text.update()
                    a += 1
                    with open('book_log\{}result.txt'.format(bookname), 'a', encoding='utf-8') as fp:
                        fp.write(
                            each_one['book_author'] +
                            ' ' +
                            each_one['book_url'] +
                            '\n')
        elif self.page_num == 0:
            MYapp.text.insert(END, "对不起，未找到此小说")
            MYapp.text.see(END)
            MYapp.text.update()
            return

        else:
            if self.page_num > 5:
                self.page_num2 = 5
                MYapp.text.insert(END, '由于页数太多，请精确搜索，此次只显示前五页')
                MYapp.text.see(END)
                MYapp.text.update()
            else:
                self.page_num2 = self.page_num
                MYapp.text.insert(END, '一共' + self.aa + '页搜索结果')
                MYapp.text.see(END)
                MYapp.text.update()
            xiaoshuo_hebing = []
            xiaoshuo_hebing1 = []
            book_hebing = []
            author_hebing = []
            book_hebing1 = []
            author_hebing1 = []
            self.a123 = []
            for i in range(1, self.page_num2 + 1):
                url2 = 'http://www.quanwenyuedu.io/index.php?c=xs&a=search&keywords=' + \
                       parse.quote(bookname) + '&page={}'.format(i)
                self.a123.append(url2)
            global pox3
            pox3 = 1
            # for url2 in self.a123:
            for i in range(1, self.page_num2 + 1):
                global pox2
                pox2 = 0
                url2 = 'http://www.quanwenyuedu.io/index.php?c=xs&a=search&keywords=' + \
                    parse.quote(bookname) + '&page={}'.format(i)
                response2 = requests.get(url2, headers=header, timeout=35)
                content2 = response2.text
                req = '<h3><a href="(.*?)">.*?</a></h3>'
                xiaoshuo_id2 = re.findall(req, content2)
                xiaoshuo_hebing.extend(xiaoshuo_id2)
                xiaoshuo_hebing1.append(xiaoshuo_id2)
                req1 = '<h3><a href=".*?">(.*?)</a></h3>'
                book_name2 = re.findall(req1, content2)
                book_hebing.extend(book_name2)
                book_hebing1.append(book_name2)
                req2 = '<p>.*?<span>(.*?)</span></p>'
                author_name2 = re.findall(req2, content2)
                author_hebing.extend(author_name2)
                author_hebing1.append(author_name2)

            self.new_url2 = []
            chapter_all_dict2 = {}
            for i in xiaoshuo_hebing:
                self.new_url123 = 'http://www.quanwenyuedu.io' + i
                self.new_url2.append(self.new_url123)
            global pox
            pox = 0

            for each in self.new_url2:
                chapter_each2 = {}
                chapter_each2['book_url'] = each  # 获取书本url
                chapter_each2['book_author'] = book_hebing[pox] + \
                    '--->' + author_hebing[pox]
                chapter_num2 = int(pox)  # 书本序号
                # 记录到所有的章节的字典中保存
                chapter_all_dict2[chapter_num2] = chapter_each2
                pox += 1
            self.pathh = r'book_log\\'
            if os.path.isdir(self.pathh):
                pass
            else:
                os.makedirs(self.pathh)
                win32api.SetFileAttributes(
                    'book_log', win32con.FILE_ATTRIBUTE_HIDDEN)
            path = r'book_log\{}result.txt'.format(bookname)
            if os.path.exists(path):
                global pob
                pob = 1
                for each in chapter_all_dict2:
                    each_one = chapter_all_dict2[each]
                    MYapp.text.insert(
                        END, str(pob) + '  ' + each_one['book_author'])
                    MYapp.text.see(END)
                    MYapp.text.update()
                    pob += 1
                # pass
            else:
                global poa
                poa = 1
                for each in chapter_all_dict2:
                    each_one = chapter_all_dict2[each]
                    MYapp.text.insert(
                        END, str(poa) + '  ' + each_one['book_author'])
                    MYapp.text.see(END)
                    MYapp.text.update()
                    poa += 1
                    with open('book_log\{}result.txt'.format(bookname), 'a', encoding='utf-8') as fp:
                        fp.write(
                            each_one['book_author'] +
                            ' ' +
                            each_one['book_url'] +
                            '\n')

    def getxinxi1(self):
        path3 = r'search_log\resultlog.txt'
        self.count2 = linecache.getline(path3, 1)
        print(self.count2)
        self.count3 = self.count2.replace('\n', '')
        self.count0 = self.count3.split(' ')[0]
        return(self.count0)

    def stop(self):
        self.isRunning = True


# 选择页数


class xuanzeyeshu(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.line = Select.entry.get()
        with open('search_log\\resultlog2.txt', 'w', encoding='utf-8') as f:
            f.write(self.line)
            f.close()
        top.destroy()

    def xiaoshuo(self, url):
            url1 = url['url']
            url2 = 'https://www.dingdiann.com/' + url1
            time.sleep(0.2)
        # try:
            header = {'Accept': '*/*',
                      'Accept-Language': 'en-US,en;q=0.8',
                      'Cache-Control': 'max-age=0',
                      'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/48.0.2564.116 Safari/537.36',
                      'Connection': 'keep-alive',
                      'Referer': url2}
            # html2 = request.urlopen(url2, timeout=10)
            # html1= html2.read().decode('utf-8')

            html123 = requests.get(
                url2,
                headers=header,
                verify=False,
                timeout=35)
            html1=html123.text

            req = '<h1>(.*?)</h1>'
            biaoti = re.findall(req, html1)
            self.biaoti2 = biaoti[0]
            rstr = r"[\/\\\:\*\?\"\<\>\|\？]"  # '/ \ : * ? " < > | ？'
            self.biaoti3 = re.sub(rstr, " ", self.biaoti2)  # 替换为空格
            req1 = '<div id="content">(.*?)</div>'
            self.title = re.findall(req1, html1, re.S)
            self.zhangjie = url2.split('/')[-1]
            self.zhangjie_xuhao = self.zhangjie.replace('.html', '')
            for i in self.title:
                self.paragraph1 = i.replace(
                    '\r\n\t\t\t\t',
                    '').replace(
                    '<br/><br/>',
                    '\n') .replace(
                    '<script>chaptererror();</script>',
                    '') .replace(
                    '打击盗版，支持正版，请到逐浪网阅读最新内容。当前用户ID:,当前用户名:',
                    '') .replace(
                    '最新全本：、、、、、、、、、、',
                    '') .replace(
                        '//Www、qb⑤、c0M//',
                        '') .replace(
                            'ＷＷw。QΒ５。ｃｏM',
                            '') .replace(
                                '&lt;&gt;.ntp*{:-:-;t:;}.ntp;n;}&lt;/&gt;',
                    ' ')
            self.write2(self.biaoti3, self.paragraph1, self.zhangjie_xuhao)
        # except BaseException:
        #     pass

    def xiaoshuo1(self, url):
        url2 = url['url']
        header = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'www.quanwenyuedu.io',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/48.0.2564.116 Safari/537.36',
            'Connection': 'keep-alive',
            'Referer': self.quanben_url2}
        try:
            # html2 = request.urlopen(url2, timeout=10)
            # html1= html2.read().decode('utf-8')
            html1 = requests.get(url2, headers=header, timeout=35).text
            req = '<h1>(.*?)</h1>'
            biaoti = re.findall(req, html1)
            self.biaoti2 = biaoti[0]
            rstr = r"[\/\\\:\*\?\"\<\>\|\？]"  # '/ \ : * ? " < > | ？'
            self.biaoti3 = re.sub(rstr, " ", self.biaoti2)  # 替换为空格
            req1 = '<div class="articlebody" id="content">(.*?)</div>'
            self.title = re.findall(req1, html1, re.S)
            self.zhangjie = url2.split('/')[-1]
            self.zhangjie_xuhao = self.zhangjie.replace('.html', '')
            for i in self.title:
                a123 = i.replace(
                    '\n<p>', '    ').replace(
                    '</p><p>&nbsp;</p><p>', '\n      ')
                par = a123.replace('<p>', '')
                self.paragraph1 = par.replace('</p>', '\n     ')  # 替换
                self.newName = self.paragraph1.replace('<!--PAGE 1-->', ' ') \
                    .replace('<!--PAGE 2-->', ' ') \
                    .replace('<!--PAGE 3-->', ' ') \
                    .replace('<!--PAGE 4-->', ' ') \
                    .replace('<!--PAGE 6-->', ' ') \
                    .replace('<!--PAGE 7-->', ' ') \
                    .replace('<!--PAGE 9-->', ' ') \
                    .replace('<!--PAGE 8-->', ' ') \
                    .replace('<!--PAGE 5-->', ' ') \
                    .replace('&nbsp;', '')\
                    .replace('『章节错误,点此举报』', '   ')
            # print(a123)
            self.write1(self.biaoti3, self.newName, self.zhangjie_xuhao)
        except BaseException:
            print('123456789')

    def xiaoshuo2(self, url):
        url2 = 'https://qxs.la' + url['url']

        header = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'qxs.la',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/48.0.2564.116 Safari/537.36',
            'Connection': 'keep-alive',
            'Referer': url2}

        try:
            # html2 = request.urlopen(url3,timeout=5)
            # html1= html2.read().decode('gbk')
            time.sleep(0.5)
            html1 = requests.get(url2, headers=header, timeout=35)
            html3 = html1.content
            html2 = str(html3, 'gbk')
            # html1.encoding='gbk'
            # html2=html1.text
            req = '<div class="text t_c"><h1>(.*?)</h1></div>'
            biaoti = re.findall(req, html2)
            self.biaoti2 = biaoti[0]
            rstr = r"[\/\\\:\*\?\"\<\>\|\？]"  # '/ \ : * ? " < > | ？'
            self.biaoti3 = re.sub(rstr, " ", self.biaoti2)  # 替换为空格
            req1 = '</script></td></tr></table>(.*?)<div style="color:'
            self.title = re.findall(req1, html2, re.S)
            self.zhangjie = url2.split('/')[-2]
            for i in self.title:
                a123 = i.replace('<br/><br/>\u3000\u3000', '\n      ')
                par = a123.replace('<br/><br/>', ' ')
                self.paragraph1 = par.replace(
                    '\r\n</div>\r\n\r\n            ', '')  # 替换
            self.write3(self.biaoti3, self.paragraph1, self.zhangjie)
        except BaseException:
            pass

    def run(self):

        # path3 = r'search_log\resultlog.txt'
        with open('search_log\\resultlog.txt', 'r', encoding='utf-8') as f:
            self.count2 = f.read()  # 用于开始下载 判断采用哪个
        # self.count2 = linecache.getline(path3, 1)
        self.count3 = self.count2.replace('\n', '')
        self.count0 = self.count3.split(' ')[0]
        # path34 = r'search_log\resultlog2.txt'
        with open('search_log\\resultlog2.txt', 'r', encoding='utf-8') as f:
            try:
                self.count = int(f.read())  # 用于开始下载 判断采用哪个
            except ValueError:
                MYapp.text.insert(END, "请输入正确页数")
                MYapp.text.see(END)
                MYapp.text.update()
                return
        # self.count = linecache.getline(path34, 1)
        self.line2 = self.count
        if self.count0 == 'dingdianxiaoshuo':
            self.count5 = self.count3.split(' ')[1]
            self.filename = 'book_log2\{}result.txt'.format(self.count5)
            self.count6 = linecache.getline(self.filename, self.line2)
            try:
                self.dingdianurl = self.count6.split(' ')[1]
            except IndexError:
                MYapp.text.insert(END, "请输入正确页数")
                MYapp.text.see(END)
                MYapp.text.update()
                return
            self.dingdian_url = self.dingdianurl.replace('\n', '')
            start1 = time.time()
            try:            #
                self.url_12 = self.geturl_2(self.dingdian_url)
                try:
                    self.url_3 = self.url_12[0]
                    pool = Pool(processes=35)
                    pool.map(self.xiaoshuo, [self.url_3[each]
                                             for each in self.url_3])  # 调用xiaoshuo 方法
                    pool.close()
                    pool.join()
                    self.hebing2()
                    MYapp.text.insert(END, '合并成功')
                    MYapp.text.see(END)
                    MYapp.text.update()
                    end1 = time.time()
                    MYapp.text.insert(END, '耗费时间：%d s' % (end1 - start1))
                    MYapp.text.see(END)
                    MYapp.text.update()
                except TypeError:
                    MYapp.text.insert(END, '网络出错，请重试')
                    MYapp.text.see(END)
                    MYapp.text.update()
            except IndexError:

                return
        elif self.count0 == 'quanbenyuedu':
            self.count51 = self.count3.split(' ')[1]
            self.filename1 = 'book_log\{}result.txt'.format(self.count51)
            self.count61 = linecache.getline(self.filename1, self.line2)
            start2 = time.time()
            try:
                quanbenurl = self.count61.split(' ')[1]
                quanben_url = quanbenurl.replace('\n', '')
                self.quanben_url2 = quanben_url + 'xiaoshuo.html'
                self.url_12 = self.geturl_1(self.quanben_url2)
                self.url_31 = self.url_12[0]

                # st= time.time()
                pool1 = Pool(processes=35)

                result = pool1.map(
                    self.xiaoshuo1, [
                        self.url_31[each] for each in self.url_31])  # 调用xiaoshuo 方法
                pool1.close()
                pool1.join()
                self.hebing1()
                MYapp.text.insert(END, '合并成功')
                MYapp.text.see(END)
                MYapp.text.update()
                end2 = time.time()
                MYapp.text.insert(END, '耗费时间：%d s' % (end2 - start2))
                MYapp.text.see(END)
                MYapp.text.update()
            except IndexError:
                MYapp.text.insert(END, "请输入正确页数")
                MYapp.text.see(END)
                MYapp.text.update()
                return
        else:
            self.count52 = self.count3.split(' ')[1]
            self.filename2 = 'book_log3\{}result.txt'.format(self.count52)
            self.count62 = linecache.getline(self.filename2, self.line2)

            try:
                self.mianfeiquanben = self.count62.split(' ')[1]
            except IndexError:
                MYapp.text.insert(END, "请输入正确页数")
                MYapp.text.see(END)
                MYapp.text.update()
                return
            self.mianfeiquanben_url = self.mianfeiquanben.replace('\n', '')
            start1 = time.time()
            try:  #
                self.url_12 = self.geturl_3(self.mianfeiquanben_url)

                self.url_3 = self.url_12[0]
                pool = Pool(processes=4)
                pool.map(self.xiaoshuo2, [self.url_3[each]
                                          for each in self.url_3])  # 调用xiaoshuo 方法
                pool.close()

                pool.join()

                self.hebing3()
                MYapp.text.insert(END, '合并成功')
                MYapp.text.see(END)
                MYapp.text.update()
                end1 = time.time()
                MYapp.text.insert(END, '耗费时间：%d s' % (end1 - start1))
                MYapp.text.see(END)
                MYapp.text.update()
            except IndexError:
                return

    def hebing1(self):
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line1 = f.readline()
            filedir = self.line1 + \
                '\全本小说网\{}\\'.format(self.newwname2)  # 获取当前文件夹中的文件名称列表
            filenames = os.listdir(filedir)  # 打开当前目录下的result.txt文件，如果没有则创建
            filenames.sort(key=lambda powx: int(powx[:-1].split()[0]))
            with open(
                self.line1 +
                '\全本小说网\{}.txt'.format(
                    self.newwname2),
                'w',
                    encoding='utf-8') as f:
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

        else:
            filedir = r'全本小说网\{}\\'.format(self.newwname2)  # 获取当前文件夹中的文件名称列表

            filenames = os.listdir(filedir)  # 打开当前目录下的result.txt文件，如果没有则创建

            filenames.sort(key=lambda powx: int(powx[:-1].split()[0]))
            with open(
                '全本小说网\{}.txt'.format(
                    self.newwname2),
                'w',
                    encoding='utf-8') as f:
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

    def geturl_1(self, url):
        header = {'Accept': '*/*',
                  'Accept-Language': 'en-US,en;q=0.8',
                  'Cache-Control': 'max-age=0',
                  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/48.0.2564.116 Safari/537.36',
                  'Connection': 'keep-alive',
                  'Referer': url}
        self.quanbenqian = url.split('xiaoshuo.html')[0]
        try:
            html = requests.get(url, headers=header, timeout=35).text
            req1 = '<p class="title"><span>(.*?)</span></p>'
            book_name = re.findall(req1, html)
            req2 = '<p>作者: <span>(.*?)</span></p>'
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
                self.patha = self.line + '\全本小说网\{}\\'.format(self.newwname2)
                if os.path.isdir(self.patha):
                    pass
                else:
                    os.makedirs(self.patha)
            else:
                self.patha = '全本小说网\{}\\'.format(self.newwname2)
                if os.path.isdir(self.patha):
                    pass
                else:
                    os.makedirs(self.patha)
            req = '<li><a href="(.*?)"'
            self.purl = re.findall(req, html)
            chapter_all_dict = {}
            global x
            x = 0
            for each in self.purl:
                chapter_each = {}
                chapter_each['url'] = self.quanbenqian + each  # 获取章节url
                chapter_num = int(x)  # 提取章节序号
                chapter_all_dict[chapter_num] = chapter_each  # 记录到所有的章节的字典中保存
                x += 1

            return chapter_all_dict, self.newwname2
        except BaseException:
            pass

    def write1(self, name, title1, zhangjie_xuhao):
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            if os.path.exists(
                    self.line +
                    '\全本小说网\{}'.format(
                        self.url_12[1]) +
                    '\{}'.format(zhangjie_xuhao) +
                    ' ' +
                    '{}.txt'.format(name)):
                MYapp.text.insert(END, '已存在：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                pass
            else:
                MYapp.text.insert(END, '正在下载：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                with open(self.line + '\全本小说网\{}'.format(self.url_12[1]) + '\{}'.format(zhangjie_xuhao) + ' ' + name + '.txt',
                          'a',
                          encoding='utf-8') as fp:
                    fp.write(name + '\n')
                    fp.write(title1)
                    time.sleep(0.08)
        else:
            if os.path.exists(
                    '全本小说网\{}'.format(
                        self.url_12[1]) +
                    '\{}'.format(zhangjie_xuhao) +
                    ' ' + '{}.txt'.format(name)):
                MYapp.text.insert(END, '已存在：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                pass
            else:

                MYapp.text.insert(END, '正在下载：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                with open('全本小说网\{}'.format(self.url_12[1]) + '\{}'.format(zhangjie_xuhao) + ' ' + name + '.txt', 'a',
                          encoding='utf-8') as fp:
                    fp.write(name + '\n' + title1)
                    time.sleep(0.08)

    def hebing2(self):
        time.sleep(0.8)
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line12 = f.readline()
            filedir = self.line12 + \
                '\顶点小说网\{}\\'.format(self.newwname2)  # 获取当前文件夹中的文件名称列表
            filenames = os.listdir(filedir)  # 打开当前目录下的result.txt文件，如果没有则创建
            filenames.sort(key=lambda powx: int(powx[:-1].split()[0]))
            with open(
                self.line12 +
                '\顶点小说网\{}.txt'.format(
                    self.newwname2),
                'w',
                    encoding='utf-8') as f:
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

        else:
            filedir = r'顶点小说网\{}\\'.format(self.newwname2)  # 获取当前文件夹中的文件名称列表

            filenames = os.listdir(filedir)  # 打开当前目录下的result.txt文件，如果没有则创建

            filenames.sort(key=lambda powx: int(powx[:-1].split()[0]))
            with open(
                '顶点小说网\{}.txt'.format(
                    self.newwname2),
                'w',
                    encoding='utf-8') as f:
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

    def geturl_2(self, url):
        header = {'Accept': '*/*',
                  'Accept-Language': 'en-US,en;q=0.8',
                  'Cache-Control': 'max-age=0',
                  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/48.0.2564.116 Safari/537.36',
                  'Connection': 'keep-alive',
                  'Referer': url}
        try:
            html = requests.get(
                url,
                headers=header,
                verify=False,
                timeout=35).text
            req1 = 'property="og:novel:book_name" content="(.*?)"/>'
            book_name = re.findall(req1, html)
            req2 = 'property="og:novel:author" content="(.*?)"/>'
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
                self.patha = self.line + '\顶点小说网\{}\\'.format(self.newwname2)
                if os.path.isdir(self.patha):
                    pass
                else:
                    os.makedirs(self.patha)
            else:
                self.patha = '顶点小说网\{}\\'.format(self.newwname2)
                if os.path.isdir(self.patha):
                    pass
                else:
                    os.makedirs(self.patha)
            req = '<a style="" href="(.*?)">'
            self.purl = re.findall(req, html)

            self.newpurl12 = []
            for i in self.purl:
                self.newpurl = i
                self.newpurl12.append(self.newpurl)
            chapter_all_dict = {}
            global x
            x = 0
            for each in self.newpurl12:
                chapter_each = {}
                chapter_each['url'] = each  # 获取章节url
                chapter_num = int(x)  # 提取章节序号
                chapter_all_dict[chapter_num] = chapter_each  # 记录到所有的章节的字典中保存
                x += 1

            return chapter_all_dict, self.newwname2
        except BaseException:
            pass

    def write2(self, name, title1, zhangjie_xuhao):
        time.sleep(0.8)
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            if os.path.exists(
                self.line +
                '\顶点小说网\{}'.format(
                    self.url_12[1]) +
                '\{}'.format(zhangjie_xuhao) +
                ' ' +
                    '{}.txt'.format(name)):
                MYapp.text.insert(END, '已存在：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                pass
            else:

                MYapp.text.insert(END, '正在下载：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                with open(self.line + '\顶点小说网\{}'.format(self.url_12[1]) + '\{}'.format(zhangjie_xuhao) + ' ' + '.txt', 'a',
                          encoding='utf-8') as fp:
                    fp.write(name + '\n' + title1)
                    # time.sleep(0.8)
        else:
            if os.path.exists(
                '顶点小说网\{}'.format(
                    self.url_12[1]) +
                '\{}'.format(zhangjie_xuhao) +
                ' ' +
                    '{}.txt'.format(name)):

                MYapp.text.insert(END, '已存在：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                pass
            else:

                MYapp.text.insert(END, '正在下载：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                with open('顶点小说网\{}'.format(self.url_12[1]) + '\{}'.format(zhangjie_xuhao) + ' ' + name + '.txt', 'a', encoding='utf-8') as fp:
                    fp.write(name + '\n' + title1)
                    # time.sleep(0.8)

    def geturl_3(self, url):
        header = {'Accept': '*/*',
                  'Accept-Language': 'en-US,en;q=0.8',
                  'Cache-Control': 'max-age=0',
                  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                                'AppleWebKit/537.36 (KHTML, like Gecko) '
                                'Chrome/48.0.2564.116 Safari/537.36',
                  'Connection': 'keep-alive',
                  'Referer': url}
        try:
            html = requests.get(
                url,
                headers=header,
                verify=False,
                timeout=35).text
            req1 = '<h1><a href="/.*?/">(.*?)</a><a'
            book_name = re.findall(req1, html)
            req2 = 'target="_blank">(.*?)</a></div>'
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
                self.patha = self.line + '\免费全本小说\{}\\'.format(self.newwname2)
                if os.path.isdir(self.patha):
                    pass
                else:
                    os.makedirs(self.patha)
            else:
                self.patha = '免费全本小说\{}\\'.format(self.newwname2)
                if os.path.isdir(self.patha):
                    pass
                else:
                    os.makedirs(self.patha)
            req = '<a href="(.*?)" title=".*?">.*?</a>'
            self.purl = re.findall(req, html)

            self.newpurl12 = []
            for i in self.purl:
                self.newpurl = i
                self.newpurl12.append(self.newpurl)
            del self.newpurl12[0:3]
            chapter_all_dict = {}
            global x
            x = 0
            for each in self.newpurl12:
                chapter_each = {}
                chapter_each['url'] = each  # 获取章节url
                chapter_num = int(x)  # 提取章节序号
                chapter_all_dict[chapter_num] = chapter_each  # 记录到所有的章节的字典中保存
                x += 1

            return chapter_all_dict, self.newwname2
        except BaseException:
            pass

    def write3(self, name, title1, zhangjie_xuhao):

        time.sleep(0.8)
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            if os.path.exists(
                self.line +
                '\免费全本小说\{}'.format(
                    self.url_12[1]) +
                '\{}'.format(zhangjie_xuhao) +
                ' ' +
                    '{}.txt'.format(name)):
                MYapp.text.insert(END, '已存在：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                pass
            else:

                MYapp.text.insert(END, '正在下载：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                with open(self.line + '\免费全本小说\{}'.format(self.url_12[1]) + '\{}'.format(zhangjie_xuhao) + ' ' + '.txt', 'a',
                          encoding='utf-8') as fp:
                    fp.write(name + '\n' + title1)
                    time.sleep(0.08)
        else:
            if os.path.exists(
                '免费全本小说\{}'.format(
                    self.url_12[1]) +
                '\{}'.format(zhangjie_xuhao) +
                ' ' +
                    '{}.txt'.format(name)):

                MYapp.text.insert(END, '已存在：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                pass
            else:

                MYapp.text.insert(END, '正在下载：{}'.format(name))
                MYapp.text.see(END)
                MYapp.text.update()
                with open('免费全本小说\{}'.format(self.url_12[1]) + '\{}'.format(zhangjie_xuhao) + ' ' + name + '.txt', 'a', encoding='utf-8') as fp:
                    fp.write(name + '\n' + title1)
                    time.sleep(0.08)

    def hebing3(self):
        time.sleep(0.8)
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line12 = f.readline()
            filedir = self.line12 + \
                '\免费全本小说\{}\\'.format(self.newwname2)  # 获取当前文件夹中的文件名称列表
            filenames = os.listdir(filedir)  # 打开当前目录下的result.txt文件，如果没有则创建
            filenames.sort(key=lambda powx: int(powx[:-1].split()[0]))
            with open(
                self.line12 +
                '\免费全本小说\{}.txt'.format(
                    self.newwname2),
                'w',
                    encoding='utf-8') as f:
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

        else:
            filedir = r'免费全本小说\{}\\'.format(self.newwname2)  # 获取当前文件夹中的文件名称列表

            filenames = os.listdir(filedir)  # 打开当前目录下的result.txt文件，如果没有则创建

            filenames.sort(key=lambda powx: int(powx[:-1].split()[0]))
            with open(
                '免费全本小说\{}.txt'.format(
                    self.newwname2),
                'w',
                    encoding='utf-8') as f:
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

    def stop(self):
        self.isRunning = True

# 奇书网整本下载http://www.qishu.cc


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
                    MYapp.text.insert(END, '正在下载小说：{}.rar'.format(bookname))
                    MYapp.text.see(END)
                    MYapp.text.update()
                    urllib.request.urlretrieve(
                        url3, self.line + '\奇书网小说\{}.rar'.format(bookname))
                    MYapp.text.insert(END, "下载完毕")
                    MYapp.text.see(END)
                    MYapp.text.update()
                except BaseException:
                    MYapp.text.insert(END, "未找到，正在尝试搜寻其他源")
                    MYapp.text.see(END)
                    MYapp.text.update()
                    try:
                        MYapp.text.insert(
                            END, '正在下载小说：{}.txt--速度较慢'.format(bookname))
                        MYapp.text.see(END)
                        MYapp.text.update()
                        urllib.request.urlretrieve(
                            url1, self.line + '奇书网小说\{}.txt'.format(bookname))
                        try:
                            urllib.request.urlretrieve(
                                url2, self.line + '奇书网小说\{}.txt'.format(bookname))
                            MYapp.text.insert(END, "下载完毕")
                            MYapp.text.see(END)
                            MYapp.text.update()
                        except BaseException:
                            pass
                    except BaseException:
                        MYapp.text.insert(END, "对不起，找到此小说")
                        MYapp.text.see(END)
                        MYapp.text.update()
        else:
            try:
                MYapp.text.insert(END, '正在下载小说：{}.rar'.format(bookname))
                MYapp.text.see(END)
                MYapp.text.update()

                urllib.request.urlretrieve(
                    url3, '奇书网小说\{}.rar'.format(bookname))
                MYapp.text.insert(END, "下载完毕")
                MYapp.text.see(END)
                MYapp.text.update()

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
                        urllib.request.urlretrieve(
                            url2, '奇书网小说\{}.txt'.format(bookname))
                        MYapp.text.insert(END, "下载完毕")
                        MYapp.text.see(END)
                        MYapp.text.update()
                    except BaseException:
                        pass
                except BaseException:
                    MYapp.text.insert(END, "对不起，找到此小说")
                    MYapp.text.see(END)
                    MYapp.text.update()

    def stop(self):
        self.isRunning = True

# 全本阅读 直接下载


class dingdianxiaoshuo(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.url1 = MYapp.entry.get()
        if self.url1 == '':
            pass
        else:
            self.pathg = r'search_log\\'

            if os.path.isdir(self.pathg):
                pass
            else:
                os.makedirs(self.pathg)
                win32api.SetFileAttributes(
                    'search_log', win32con.FILE_ATTRIBUTE_HIDDEN)
                # win32api.SetFileAttributes('search_log', win32con.FILE_ATTRIBUTE_READONLY)
            with open('search_log\\resultlog.txt', 'w', encoding='utf-8') as f:
                f.write('dingdianxiaoshuo ' + self.url1)

    def run(self):
        if self.url1 == '':
            MYapp.text.insert(END, '请输入小说名称')
            MYapp.text.see(END)
            MYapp.text.update()
            return
        self.search_book(self.url1)

    def search_book(self, bookname):
        url = 'https://www.dingdiann.com/searchbook.php?keyword=' + \
              parse.quote(bookname)
        header = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'private',
            'Host': 'www.dingdiann.com',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/48.0.2564.116 Safari/537.36',
            'Connection': 'keep-alive',
            'Referer': url
        }
        try:
            response = requests.get(
                url, headers=header, verify=False, timeout=35)
            content = response.text
        except requests.exceptions.ConnectionError:
            MYapp.text.insert(END, "请检查网络连接")
            MYapp.text.see(END)
            MYapp.text.update()
            return
        try:
            req5 = '<em id="pagestats">(.*?)</em>'
            page = re.findall(req5, content)[0]
        except IndexError:
            MYapp.text.insert(END, "对不起，未找到此小说")
            MYapp.text.see(END)
            MYapp.text.update()
            return
        self.aa = page.split('/')[1]
        self.page_num = int(self.aa)
        if self.page_num == 1:
            req = 'class="s2"><a href="(.*?)"'
            xiaoshuo_id = re.findall(req, content)
            req1 = 'target="_blank">(.*?)</a></span><span'
            book_name = re.findall(req1, content)
            req2 = 'class="s4">(.*?)</span>'
            author_name = re.findall(req2, content)
            self.new_url = []
            chapter_all_dict = {}
            for i in xiaoshuo_id:
                self.newurl = 'https://www.dingdiann.com' + i
                self.new_url.append(self.newurl)
            global x
            global y
            y = 0
            x = 0
            for each in self.new_url:
                chapter_each = {}
                chapter_each['book_url'] = each  # 获取书本url
                chapter_each['book_author'] = book_name[x] + \
                    '--->' + author_name[y + 1]
                chapter_num = int(y)  # 书本序号
                chapter_all_dict[chapter_num] = chapter_each  # 记录到所有的章节的字典中保存
                x += 2
                y += 1
            self.pathh = r'book_log2\\'
            if os.path.isdir(self.pathh):
                pass
            else:
                os.makedirs(self.pathh)
                win32api.SetFileAttributes(
                    'book_log2', win32con.FILE_ATTRIBUTE_HIDDEN)
            path = r'book_log2\{}result.txt'.format(bookname)
            if os.path.exists(path):
                global b
                b = 1
                for each in chapter_all_dict:
                    each_one = chapter_all_dict[each]
                    MYapp.text.insert(
                        END, str(b) + '  ' + each_one['book_author'])
                    MYapp.text.see(END)
                    MYapp.text.update()
                    b += 1
            else:
                global a
                a = 1
                for each in chapter_all_dict:
                    each_one = chapter_all_dict[each]
                    MYapp.text.insert(
                        END, str(a) + '  ' + each_one['book_author'])
                    MYapp.text.see(END)
                    MYapp.text.update()
                    a += 1
                    with open('book_log2\{}result.txt'.format(bookname), 'a', encoding='utf-8') as fp:
                        fp.write(
                            each_one['book_author'] +
                            ' ' +
                            each_one['book_url'] +
                            '\n')
        else:
            if self.page_num > 5:
                self.page_num2 = 5
                MYapp.text.insert(END, '由于页数太多，请精确搜索，此次只显示前五页')
                MYapp.text.see(END)
                MYapp.text.update()
            else:
                self.page_num2 = self.page_num
                MYapp.text.insert(END, '一共' + self.aa + '页搜索结果')
                MYapp.text.see(END)
                MYapp.text.update()
            xiaoshuo_hebing = []
            xiaoshuo_hebing1 = []
            book_hebing = []
            author_hebing = []
            book_hebing1 = []
            author_hebing1 = []
            self.a123 = []
            for i in range(1, self.page_num2 + 1):
                url2 = 'https://www.dingdiann.com/searchbook.php?keyword=' + \
                       parse.quote(bookname) + '&page={}'.format(i)
                self.a123.append(url2)
            global pox3
            pox3 = 1
            for i in range(1, self.page_num2 + 1):
                global pox2
                pox2 = 0
                url2 = 'https://www.dingdiann.com/searchbook.php?keyword=' + \
                       parse.quote(bookname) + '&page={}'.format(i)
                response2 = requests.get(
                    url2, headers=header, verify=False, timeout=35)
                content2 = response2.text
                req = 'class="s2"><a href="(.*?)"'
                xiaoshuo_id2 = re.findall(req, content2)
                xiaoshuo_hebing.extend(xiaoshuo_id2)
                xiaoshuo_hebing1.append(xiaoshuo_id2)
                req1 = 'target="_blank">(.*?)</a></span><span'
                book_name2 = re.findall(req1, content2)
                book_hebing.extend(book_name2)
                book_hebing1.append(book_name2)
                req2 = 'class="s4">(.*?)</span>'
                author_name2 = re.findall(req2, content2)
                author_hebing.extend(author_name2)
                author_hebing1.append(author_name2)
            self.new_url2 = []
            chapter_all_dict2 = {}
            for i in xiaoshuo_hebing:
                self.new_url123 = 'https://www.dingdiann.com' + i
                self.new_url2.append(self.new_url123)
            global pox
            global poy
            global poz
            poz = 0
            poy = 0
            pox = 0
            for each in self.new_url2:
                chapter_each2 = {}
                chapter_each2['book_url'] = each  # 获取书本url
                # if pox ==
                if poz == 30 or poz == 61 or poz == 92 or poz == 123:
                    chapter_each2['book_author'] = book_hebing[pox] + \
                        '--->' + author_hebing[poz + 2]
                    poz += 2

                else:
                    chapter_each2['book_author'] = book_hebing[pox] + \
                        '--->' + author_hebing[poz + 1]
                    poz += 1
                chapter_num2 = int(poy)  # 书本序号
                # 记录到所有的章节的字典中保存
                chapter_all_dict2[chapter_num2] = chapter_each2

                poy += 1
                pox += 2

            self.pathh = r'book_log2\\'
            if os.path.isdir(self.pathh):
                pass
            else:
                os.makedirs(self.pathh)
                win32api.SetFileAttributes(
                    'book_log2', win32con.FILE_ATTRIBUTE_HIDDEN)
            path = r'book_log2\{}result.txt'.format(bookname)
            if os.path.exists(path):
                global pob
                pob = 1
                for each in chapter_all_dict2:
                    each_one = chapter_all_dict2[each]
                    MYapp.text.insert(
                        END, str(pob) + '  ' + each_one['book_author'])
                    MYapp.text.see(END)
                    MYapp.text.update()
                    pob += 1
                # pass
            else:
                global poa
                poa = 1
                for each in chapter_all_dict2:
                    each_one = chapter_all_dict2[each]
                    MYapp.text.insert(
                        END, str(poa) + '  ' + each_one['book_author'])
                    MYapp.text.see(END)
                    MYapp.text.update()
                    poa += 1
                    with open('book_log2\{}result.txt'.format(bookname), 'a', encoding='utf-8') as fp:
                        fp.write(
                            each_one['book_author'] +
                            ' ' +
                            each_one['book_url'] +
                            '\n')

    def stop(self):
        self.isRunning = True


class __fun(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.NAME = MYapp.entry.get()
        if self.NAME == '':
            pass
        else:
            self.pathg = r'search_log\\'

            if os.path.isdir(self.pathg):
                pass
            else:
                os.makedirs(self.pathg)
                win32api.SetFileAttributes(
                    'search_log', win32con.FILE_ATTRIBUTE_HIDDEN)
                # win32api.SetFileAttributes('search_log', win32con.FILE_ATTRIBUTE_READONLY)
            with open('search_log\\resultlog.txt', 'w', encoding='utf-8') as f:
                f.write('5200quanben ' + self.NAME)

    def run(self):
        if self.NAME == '':
            MYapp.text.insert(END, '请输入小说名称')
            MYapp.text.see(END)
            MYapp.text.update()
            return
        self.search(self.NAME)

    def search(self, bookname):

        url = 'https://qxs.la/s_' + \
              parse.quote(bookname)
        header = {
            'Accept': '*/*',
            'Accept-Language': 'en-US,en;q=0.8',
            'Cache-Control': 'private',
            'Host': 'qxs.la',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/48.0.2564.116 Safari/537.36',
            'Connection': 'keep-alive',
            'Referer': url
        }
        try:
            response = requests.get(
                url, headers=header, verify=False, timeout=35)
            content = response.text
        except requests.exceptions.ConnectionError:
            MYapp.text.insert(END, "请检查网络连接")
            MYapp.text.see(END)
            MYapp.text.update()
            return
        try:
            req6 = '<div id="pagenav"><a class="current">(.*?)</a>'
            page = re.findall(req6, content)[0]

        except IndexError:
            MYapp.text.insert(END, "对不起，未找到此小说")
            MYapp.text.see(END)
            MYapp.text.update()
            return
        aa = [page]
        req5 = '<a href="/s_' + '{}'.format(bookname) + '/(.*?)/">'
        page = re.findall(req5, content)
        global xxx
        xxx = 1
        for i in page:
            aa.append(i)
            xxx += 1
        self.page_num3 = xxx

        self.page_num = int(self.page_num3)
        if self.page_num == 1:
            req = '<li class="cc2"><a href="/(.*?)/">'
            xiaoshuo_id = re.findall(req, content)
            req1 = '<li class="cc2"><a href="/.*?/">(.*?)</a></li>'
            book_name = re.findall(req1, content)
            req2 = '<li class="cc4"><a href="//qxs.la/zuozhe/.*?">(.*?)</a></li>'
            author_name = re.findall(req2, content)
            self.new_url = []
            chapter_all_dict = {}
            for i in xiaoshuo_id:
                self.newurl = 'https://qxs.la/' + i + '/'
                self.new_url.append(self.newurl)
            global x
            global y
            y = 0
            x = 0
            for each in self.new_url:
                chapter_each = {}
                chapter_each['book_url'] = each  # 获取书本url
                chapter_each['book_author'] = book_name[x] + \
                    '--->' + author_name[y]
                chapter_num = int(y)  # 书本序号
                chapter_all_dict[chapter_num] = chapter_each  # 记录到所有的章节的字典中保存
                x += 1
                y += 1
            self.pathh = r'book_log3\\'
            if os.path.isdir(self.pathh):
                pass
            else:
                os.makedirs(self.pathh)
                win32api.SetFileAttributes(
                    'book_log3', win32con.FILE_ATTRIBUTE_HIDDEN)
            path = r'book_log3\{}result.txt'.format(bookname)
            if os.path.exists(path):
                global b
                b = 1
                for each in chapter_all_dict:
                    each_one = chapter_all_dict[each]
                    MYapp.text.insert(
                        END, str(b) + '  ' + each_one['book_author'])
                    MYapp.text.see(END)
                    MYapp.text.update()
                    b += 1
            else:
                global a
                a = 1
                for each in chapter_all_dict:
                    each_one = chapter_all_dict[each]
                    MYapp.text.insert(
                        END, str(a) + '  ' + each_one['book_author'])
                    MYapp.text.see(END)
                    MYapp.text.update()
                    a += 1
                    with open('book_log3\{}result.txt'.format(bookname), 'a', encoding='utf-8') as fp:
                        fp.write(
                            each_one['book_author'] +
                            ' ' +
                            each_one['book_url'] +
                            '\n')
        else:
            if self.page_num > 5:
                self.page_num2 = 5
                MYapp.text.insert(END, '由于页数太多，请精确搜索，此次只显示前五页')
                MYapp.text.see(END)
                MYapp.text.update()
            else:
                self.page_num2 = self.page_num
                MYapp.text.insert(END, '一共' + str(self.page_num2) + '页搜索结果')
                MYapp.text.see(END)
                MYapp.text.update()
            xiaoshuo_hebing = []
            xiaoshuo_hebing1 = []
            book_hebing = []
            author_hebing = []
            book_hebing1 = []
            author_hebing1 = []
            self.a123 = []
            for i in range(1, self.page_num2 + 1):
                url2 = 'https://qxs.la/s_' + \
                       parse.quote(bookname) + '/{}/'.format(i)
                self.a123.append(url2)
            global pox3
            pox3 = 1
            for i in range(1, self.page_num2 + 1):
                global pox2
                pox2 = 0
                url2 = 'https://qxs.la/s_' + \
                       parse.quote(bookname) + '/{}/'.format(i)
                response2 = requests.get(
                    url2, headers=header, verify=False, timeout=35)
                content2 = response2.text
                req = '<li class="cc2"><a href="/(.*?)/">'
                xiaoshuo_id2 = re.findall(req, content2)
                xiaoshuo_hebing.extend(xiaoshuo_id2)
                xiaoshuo_hebing1.append(xiaoshuo_id2)
                req1 = '<li class="cc2"><a href="/.*?/">(.*?)</a></li>'
                book_name2 = re.findall(req1, content2)
                book_hebing.extend(book_name2)
                book_hebing1.append(book_name2)
                req2 = '<li class="cc4"><a href="//qxs.la/zuozhe/.*?">(.*?)</a></li>'
                author_name2 = re.findall(req2, content2)
                author_hebing.extend(author_name2)
                author_hebing1.append(author_name2)

            self.new_url2 = []
            chapter_all_dict2 = {}
            for i in xiaoshuo_hebing:
                self.new_url123 = 'https://qxs.la/' + i + '/'
                self.new_url2.append(self.new_url123)
            global pox
            global poy
            global poz
            poz = 0
            poy = 0
            pox = 0
            for each in self.new_url2:
                chapter_each2 = {}
                chapter_each2['book_url'] = each  # 获取书本url
                # if pox ==

                chapter_each2['book_author'] = book_hebing[pox] + \
                    '--->' + author_hebing[poz]
                poz += 1
                chapter_num2 = int(poy)  # 书本序号
                # 记录到所有的章节的字典中保存
                chapter_all_dict2[chapter_num2] = chapter_each2

                poy += 1
                pox += 1

            self.pathh = r'book_log3\\'
            if os.path.isdir(self.pathh):
                pass
            else:
                os.makedirs(self.pathh)
                win32api.SetFileAttributes(
                    'book_log3', win32con.FILE_ATTRIBUTE_HIDDEN)
            path = r'book_log3\{}result.txt'.format(bookname)
            if os.path.exists(path):
                global pob
                pob = 1
                for each in chapter_all_dict2:
                    each_one = chapter_all_dict2[each]
                    MYapp.text.insert(
                        END, str(pob) + '  ' + each_one['book_author'])
                    MYapp.text.see(END)
                    MYapp.text.update()
                    pob += 1
                # pass
            else:
                global poa
                poa = 1
                for each in chapter_all_dict2:
                    each_one = chapter_all_dict2[each]
                    MYapp.text.insert(
                        END, str(poa) + '  ' + each_one['book_author'])
                    MYapp.text.see(END)
                    MYapp.text.update()
                    poa += 1
                    with open('book_log3\{}result.txt'.format(bookname), 'a', encoding='utf-8') as fp:
                        fp.write(
                            each_one['book_author'] +
                            ' ' +
                            each_one['book_url'] +
                            '\n')

    def stop(self):
        self.isRunning = True


def download():
    test = haianxian()
    test.setDaemon(True)
    test.start()


def download2():
    test = biquge()
    test.setDaemon(True)
    test.start()


def download3():
    test = quanbenyuedu()
    test.setDaemon(True)
    test.start()


def download4():
    test = xuanzeyeshu()
    test.setDaemon(True)
    test.start()


def download5():
    test = qishuwang()
    test.setDaemon(True)
    test.start()


def download6():
    test = dingdianxiaoshuo()
    test.setDaemon(True)
    test.start()


def download7():
    test = __fun()
    test.setDaemon(True)
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
    menu1 = Menu(app, tearoff=0)

    def qingkong():
        MYapp.text.delete('0', 'end')  # 清除文本框内容
    menu1.add_command(label="清空列表", command=qingkong)

    def popupmenu1(event):
        menu1.post(event.x_root, event.y_root)
    MYapp.text.bind("<Button-3>", popupmenu1)
    app.mainloop()
