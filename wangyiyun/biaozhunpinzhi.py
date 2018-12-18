#!/usr/bin/python
# -*- coding:utf-8 -*- 1
# @Time   : 2018/7/14 0014 16:43
# @Author : wangyulin
# @File   : 网易下载器升级版.py
from tkinter import *
import psutil
from tkinter.filedialog import askdirectory
from tkinter import ttk
from urllib.request import urlretrieve
from tkinter import messagebox
import urllib,os,re,urllib.request,requests,json,time,threading
from bs4 import BeautifulSoup
class MyApp(Tk):
    def __init__(self):
        super().__init__()
        self.wm_title('网易云音乐下载 BY wangyulin')
        sw = self.winfo_screenwidth()  # 得到屏幕宽度
        sh = self.winfo_screenheight()  # 得到屏幕高度
        ww = 550
        wh = 415
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        # self.iconbitmap('icons\\format.ico')
        # 图标
        self.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
        self.resizable(width=False, height=False)
        # 设置不可改变窗口大小
        self.attributes("-alpha", 1)
        # 背景虚化
        self["bg"] = "white"
        # 设置窗口的背景颜色
        self.protocol('WM_DELETE_WINDOW', self.destroy)
        # 绑定窗口退出事件
        self.setupui()

    @staticmethod
    def clear():
        MyApp.text.delete('0', 'end')

    @staticmethod
    def open():
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                line = f.readline()
            os.startfile(line)
            # 打开路径
        else:
            path = os.path.abspath(os.curdir)
            os.startfile(path)

    @staticmethod
    def inputclear():
        MyApp.entry.delete('0', 'end')
        # 清除文本框内容

    def setupui(self):
        # 设置窗口UI
        # StringVar()  # 这即是输入框中的内容
        # url.set('')  # 通过var.get()/var.set() 来 获取/设置var的值
        lable = Label(self, text='输入网易云链接或ID', font=('楷体', 20))
        lable.grid(row=0, column=0)
        lable = Label(self, text='输入网易云链接或ID', font=('楷体', 20))
        lable.grid(row=0, column=0)
        MyApp.url = StringVar()
        MyApp.entry = Entry(
            self, textvariable=MyApp.url, font=(
                '微软雅黑', 15), width=23)
        MyApp.entry.grid(row=0, column=1)
        MyApp.text = Listbox(self, font=('微软雅黑', 15), width=45, height=10)
        MyApp.text.grid(row=1, columnspan=2)
        button = Button(
            self, text='单曲下载', font=(
                '微软雅黑', 15), command=button1_download)
        button.place(x=5, y=316.5, width=100, height=45)
        button = Button(
            self, text='歌手下载', font=(
                '微软雅黑', 15), command=button2_download)
        button.place(x=110, y=316.5, width=100, height=45)
        button = Button(
            self, text='打开文件', font=(
                '微软雅黑', 15), command=self.open)
        button.place(x=110, y=365, width=100, height=45)
        button = Button(
            self, text='歌单下载', font=(
                '微软雅黑', 15), command=button3_download)
        button.place(x=220, y=316.5, width=100, height=45)
        button = Button(
            self, text='清除链接', font=(
                '微软雅黑', 15), command=self.inputclear)
        button.place(x=220, y=365, width=100, height=45)
        button = Button(
            self, text='暂停下载', font=(
                '微软雅黑', 15), command=button4_pause)
        button.place(x=330, y=316.5, width=100, height=45)
        button = Button(self, text='继续下载', font=('微软雅黑', 15))
        button.place(x=330, y=365, width=100, height=45)
        fu = Local()
        button = Button(
            self, text='路径选择', font=(
                '微软雅黑', 15), command=fu.lujing)
        button.place(x=445, y=316.5, width=100, height=45)
        button = Button(
            self, text='清空列表', font=(
                '微软雅黑', 15), command=self.clear)
        button.place(x=5, y=365, width=100, height=45)
        button = Button(
            self, text='强制退出', font=(
                '微软雅黑', 15), command=self.destroy)
        button.place(x=445, y=365, width=100, height=45)
class section:
     def onPaste(self):
        try:
            self.text = app.clipboard_get()
        except TclError:
            pass
        MyApp.url.set(str(self.text))
     def onCopy(self):
        self.text = MyApp.entry.get()
        app.clipboard_append(self.text)
     def onCut(self):
        self.onCopy()
        try:
            MyApp.entry.delete('sel.first', 'sel.last')
        except TclError:
            pass
class Local:
    def __init__(self):
        super().__init__()

    @staticmethod
    def lujing():
        Local.path_ = askdirectory()
        if os.path.exists(Local.path_):
            with open('log.txt', 'w', encoding='utf-8') as fp:
                fp.write(Local.path_)
        else:
            pass
class THread1(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.url1=MyApp.entry.get()  #
        self.singer_id = self.url1.split('=')[-1]
        self.start_url = 'https://music.163.com/song?id={}'.format(self.singer_id)
        self.html = self.get_html(self.start_url)
        self.song_name = self.get_song_name(self.html)
    def run(self):
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            self.patha = self.line + '\单曲下载\歌词'
            self.pathb = self.line + '\单曲下载\歌曲'
            if os.path.isdir(self.patha):
                pass
            else:
                os.makedirs(self.patha)
            if os.path.isdir(self.pathb):
                pass
            else:
                os.makedirs(self.pathb)
        else:
            self.patha = r'单曲下载\歌词\\'
            self.pathb = r'单曲下载\歌曲\\'
            if os.path.isdir(self.patha):
                pass
            else:
                os.makedirs(self.patha)
            # path = r'单曲下载\歌曲\\'
            if os.path.isdir(self.pathb):
                pass
            else:
                os.makedirs(self.pathb)
        self.r = requests.get(self.start_url)
        hh = self.r.url
        if hh == 'https://music.163.com/404':
            MyApp.text.insert(END, '对不起，歌曲出错')
            MyApp.text.see(END)
            MyApp.text.update()
        else:
            lyric = self.get_lyric(self.singer_id)
            self.write_lyric(self.song_name, lyric)
            self.download_song(self.song_name, self.singer_id)
            MyApp.text.insert(END, '任务已经完成(*￣▽￣)y ')
            MyApp.text.see(END)
            MyApp.text.update()
    def get_html(self,url):
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        try:
            self.response = requests.get(url, headers=self.header)
            self.html = self.response.text
            return self.html
        except:
            MyApp.text.insert(END,"解析错误")
            MyApp.text.see(END)
            MyApp.text.update()
            pass
    def get_song_name(self,html):
        self.soup = BeautifulSoup(html, "lxml")
        self.soup1 = self.soup.find('title')
        for i in self.soup1:
            self.song_name = i.split('-')[0]
            rstr = r"[\/\\\:\*\?\"\<\>\|\？]"  # '/ \ : * ? " < > | ？'
            self.newName = re.sub(rstr, " ", self.song_name)  # 替换为空格
            return self.newName
    def get_lyric(self,song_id):
        self.lrc_url = 'http://music.163.com/api/song/lyric?id=' + str(song_id) + '&lv=1&kv=1&tv=-1'
        self.html1 = self.get_html(self.lrc_url)
        j = json.loads(self.html1)
        try:  # 部分歌曲没有歌词，这里引入一个异常
            lrc = j['lrc']['lyric']
            pat = re.compile(r'\[.*\]')
            lrc = re.sub(pat, "", lrc)
            lrc.strip()
            return lrc
        except KeyError as e:
            lrc = 0
            pass
            return lrc
    def write_lyric(self, song_name, lyric):
        if lyric == 0:
            MyApp.text.insert(END, '这首没有歌词:{}'.format(song_name))
            MyApp.text.see(END)
            MyApp.text.update()
            pass
        else:
            path2 = r'log.txt'
            if os.path.exists(path2):
                with open('log.txt', 'r', encoding='utf-8') as f:
                    self.line = f.readline()
                if os.path.exists(
                        self.line + '\单曲下载\歌词\\{}.txt'.format(song_name)):
                    MyApp.text.insert(END, '歌词已存在：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    pass
                else:
                    MyApp.text.insert(END, '正在下载歌词：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    with open(self.line + '\单曲下载\歌词\\{}.txt'.format(song_name), 'a', encoding='utf-8') as fp:
                        fp.write(lyric)
            else:
                if os.path.exists('单曲下载\歌词\{}.txt'.format(song_name)):
                    MyApp.text.insert(END, '歌词已存在：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    pass
                else:
                    MyApp.text.insert(END, '正在下载歌词：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    with open('单曲下载\歌词\\{}.txt'.format(song_name), 'a', encoding='utf-8') as fp:
                        fp.write(lyric)
    def download_song(self,song_name, song_id):
        self.singer_url = 'https://music.163.com/song/media/outer/url?id={}.mp3'.format(song_id)
        self.r = requests.get(self.singer_url)
        hh = self.r.url
        if hh == 'http://music.163.com/404':
            MyApp.text.insert(END,'版权问题，无法下载：{}'.format(song_name))
            MyApp.text.see(END)
            MyApp.text.update()
        else:
            path2 = r'log.txt'
            if os.path.exists(path2):
                with open('log.txt', 'r', encoding='utf-8') as f:
                    self.line = f.readline()
                if os.path.exists(self.line + '\单曲下载\歌曲\{}.mp3'.format(song_name)):
                    MyApp.text.insert(END, '歌曲已存在：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    pass
                else:
                    MyApp.text.insert(END, '正在下载歌曲：{}'.format(song_name))
                    urllib.request.urlretrieve(self.singer_url, self.line + '\单曲下载\歌曲\\{}.mp3'.format(song_name))
            else:
                if os.path.exists('单曲下载\歌曲\{}.mp3'.format(song_name)):
                    MyApp.text.insert(END, '歌曲已存在：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    pass
                else:
                    MyApp.text.insert(END, '正在下载歌曲：{}'.format(song_name))
                    urllib.request.urlretrieve(self.singer_url, '单曲下载\歌曲\\{}.mp3'.format(song_name))
    def stop(self):
         self.isRunning=True
class THread2(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.url1=MyApp.entry.get()  #
        self.singer_id = self.url1.split('=')[-1]
        self.start_url = 'https://music.163.com/artist?id={}'.format(self.singer_id)
        self.html = self.get_html(self.start_url)
        self.get_information = self.get_singer_info(self.html)
    def run(self):
        self.r = requests.get(self.start_url)
        hh = self.r.url
        if hh == 'https://music.163.com/404':
            MyApp.text.insert(END,'对不起，歌手歌单出错')
            MyApp.text.see(END)
            MyApp.text.update()
        else:
            MyApp.text.insert(END, '歌单中共有{}首歌曲需要下载'.format(len(self.song_IDs)))
            MyApp.text.see(END)
            MyApp.text.update()
            for self.singer_info in self.get_information:
                lyric = self.get_lyric(self.singer_info[1])
                self.write_lyric(self.singer_info[0], lyric)
                self.downloadsong(self.singer_info[0], self.singer_info[1])
            MyApp.text.insert(END, '所有任务已经下载完毕')
            MyApp.text.see(END)
            MyApp.text.update()
    def get_html(self,url):
        self.header = {'Accept': '*/*', 'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language':   'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4', 'Connection': 'keep-alive',
            'Content-Type':      'application/x-www-form-urlencoded', 'Host': 'music.163.com',
            'Referer':           'http://music.163.com/search/', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                                                                               'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        try:
                self.response = requests.get(url, headers=self.header)
                self.html = self.response.text
                return self.html
        except:
                MyApp.text.insert(END, "解析错误")
                MyApp.text.see(END)
                MyApp.text.update()
                pass
    def get_singer_info(self,html):
        self.soup = BeautifulSoup(html, "lxml")
        self.links = self.soup.find('ul', class_='f-hide').find_all('a')
        self.song_IDs = []
        for link in self.links:
            song_ID = link.get('href').split('=')[-1]
            self.song_IDs.append(song_ID)
        res = r'<ul class="f-hide">(.*?)</ul>'
        result = re.findall(res, html, re.S | re.M)
        for i in result:
            req = r'<li><a href=".*?">(.*?)</a>'
            result2 = re.findall(req, i)
            self.newwname = []
            for i in result2:
                rstr = r"[\/\\\:\*\?\"\<\>\|\？]"  # '/ \ : * ? " < > | ？'
                newName = re.sub(rstr, " ", i)  # 替换为空格
                self.newwname.append(newName)
            return zip(self.newwname, self.song_IDs)
    def get_singer_info2(self,playlist):
        global purl
        global purl2
        soup = BeautifulSoup(playlist, "lxml")
        links = soup.find('script')
        for i in links:
            req = '"title": "(.*?)"'
            purl = re.findall(req, i)
        for i in purl:
            rstr = r"[\/\\\:\*\?\"\<\>\|\？]"  # '/ \ : * ? " < > | ？'
            purl2 = re.sub(rstr, "", i)  # 替换为空格
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            self.pathe = self.line + '\歌手下载\{}\歌词\\'.format(purl2)
            self.pathf = self.line + '\歌手下载\{}\歌曲\\'.format(purl2)
            if os.path.isdir(self.pathe):
                pass
            else:
                os.makedirs(self.pathe)
            if os.path.isdir(self.pathf):
                pass
            else:
                os.makedirs(self.pathf)
            return purl2
        else:
            self.pathe = r'歌手下载\{}\歌词\\'.format(purl2)
            if os.path.isdir(self.pathe):
                pass
            else:
                os.makedirs(self.pathe)
            self.pathf = r'歌手下载\{}\歌曲\\'.format(purl2)
            if os.path.isdir(self.pathf):
                pass
            else:
                os.makedirs(self.pathf)
            return purl2

    def get_lyric(self,song_id):
        self.lrc_url = 'http://music.163.com/api/song/lyric?id=' + str(song_id) + '&lv=1&kv=1&tv=-1'
        self.html = self.get_html(self.lrc_url)
        j = json.loads(self.html)
        try:  # 部分歌曲没有歌词，这里引入一个异常
            lrc = j['lrc']['lyric']
            pat = re.compile(r'\[.*\]')
            lrc = re.sub(pat, "", lrc)
            lrc.strip()
            return lrc
        except KeyError as e:
            lrc = 0
            pass
            return lrc
    def write_lyric(self, song_name, lyric):
        html = self.get_html(self.start_url)
        singer_name3 = self.get_singer_info2(html)
        if lyric == 0:
            MyApp.text.insert(END, '这首没有歌词：{}'.format(song_name))
            MyApp.text.see(END)
            MyApp.text.update()
            pass
        else:
            path2 = r'log.txt'
            if os.path.exists(path2):
                with open('log.txt', 'r', encoding='utf-8') as f:
                    self.line = f.readline()
                if os.path.exists(
                    self.line +
                    '\歌手下载\{}\歌词'.format(singer_name3) +
                        '\{}.txt'.format(song_name)):
                    MyApp.text.insert(END, '歌词已存在：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    pass
                else:
                    MyApp.text.insert(END, '正在下载歌词：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    with open(self.line + '\歌手下载\{}\歌词'.format(singer_name3) + '\{}.txt'.format(song_name), 'a',
                              encoding='utf-8') as fp:
                        fp.write(lyric)
            else:
                if os.path.exists(
                    '歌手下载\{}\歌词'.format(singer_name3) +
                        '\{}.txt'.format(song_name)):
                    MyApp.text.insert(END, '歌词已存在：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    pass
                else:
                    MyApp.text.insert(END, '正在下载歌词：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    with open('歌手下载\{}\歌词'.format(singer_name3) + '\{}.txt'.format(song_name), 'a',
                              encoding='utf-8') as fp:
                        fp.write(lyric)
    def downloadsong(self,song_name, song_id):
        self.singer_url = 'https://music.163.com/song/media/outer/url?id={}.mp3'.format(song_id)
        html = self.get_html(self.start_url)
        singer_name3=self.get_singer_info2(html)
        self.r = requests.get(self.singer_url)
        hh = self.r.url
        if hh == 'http://music.163.com/404':
        #
            MyApp.text.insert(END,'版权问题，无法下载：{}'.format(song_name))
            MyApp.text.see(END)
            MyApp.text.update()
        else:
            path2 = r'log.txt'
            if os.path.exists(path2):
                with open('log.txt', 'r', encoding='utf-8') as f:
                    self.line = f.readline()
                if os.path.exists(
                    self.line +
                    '\歌手下载\{}\歌曲'.format(singer_name3) +
                        '\{}.mp3'.format(song_name)):
                    MyApp.text.insert(END, '歌曲已存在：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    pass
                else:
                    MyApp.text.insert(END, '正在下载歌曲：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    urllib.request.urlretrieve(
                        self.singer_url,
                        self.line +
                        '\歌手下载\{}\歌曲'.format(singer_name3) +
                        '\{}.mp3'.format(song_name))
            else:
                if os.path.exists(
                    '歌手下载\{}\歌曲'.format(singer_name3) +
                        '\{}.mp3'.format(song_name)):
                    MyApp.text.insert(END, '歌曲已存在：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    pass
                else:
                    MyApp.text.insert(END, '正在下载歌曲：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    urllib.request.urlretrieve(
                        self.singer_url,
                        '歌手下载\{}\歌曲'.format(singer_name3) +
                        '\{}.mp3'.format(song_name))
    def stop(self):
         self.isRunning=True
class THread3(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.url1=MyApp.entry.get()  #
        self.singer_id = self.url1.split('=')[-1]
        self.start_url = 'https://music.163.com/playlist?id={}'.format(self.singer_id)
        self.html = self.get_html(self.start_url)
        self.get_information = self.get_singer_info(self.html)
    def run(self):
        self.r = requests.get(self.start_url)
        self.hh = self.r.url
        if self.hh == 'https://music.163.com/404':
            MyApp.text.insert(END,'对不起，列表歌单出错')
        else:
            MyApp.text.insert(END, '歌单中共有{}首歌曲需要下载'.format(len(self.song_IDs)))
            MyApp.text.see(END)
            MyApp.text.update()
            for self.singer_info in self.get_information:
                lyric = self.get_lyric(self.singer_info[1])
                self.write_lyric(self.singer_info[0], lyric)
                self.downloadsong(self.singer_info[0], self.singer_info[1])
            MyApp.text.insert(END, '所有任务已经下载完毕')
            MyApp.text.see(END)
            MyApp.text.update()
    def get_html(self,url):
        self.header = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
        try:
                self.response = requests.get(url, headers=self.header)
                self.html = self.response.text
                return self.html
        except:
                MyApp.text.insert(END, "解析错误")
                MyApp.text.see(END)
                MyApp.text.update()
                pass
    def get_singer_info(self,html):
        self.soup = BeautifulSoup(html, "lxml")
        self.links = self.soup.find('ul', class_='f-hide').find_all('a')
        self.song_IDs = []
        for link in self.links:
            song_ID = link.get('href').split('=')[-1]
            self.song_IDs.append(song_ID)
        res = r'<ul class="f-hide">(.*?)</ul>'#<li><a href=".*?>
        result = re.findall(res, html, re.S | re.M)
        for i in result:
            req = r'<li><a href=".*?">(.*?)</a>'
            result2 = re.findall(req, i)
            self.newwname = []
            for i in result2:
                rstr = r"[\/\\\:\*\?\"\<\>\|\？]"  # '/ \ : * ? " < > | ？'
                newName = re.sub(rstr, " ", i)  # 替换为空格
                self.newwname.append(newName)
            return zip(self.newwname, self.song_IDs)
    def get_singer_info2(self,playlist):
        global purl
        global purl2
        soup = BeautifulSoup(playlist, "lxml")
        links = soup.find('script')
        for i in links:
            req = '"title": "(.*?)"'
            purl = re.findall(req, i)
        for i in purl:
            rstr = r"[\/\\\:\*\?\"\<\>\|\？]"  # '/ \ : * ? " < > | ？'
            purl2 = re.sub(rstr, "", i)  # 替换为空格
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            self.pathc = self.line + '\歌单下载\{}\歌词\\'.format(purl2)
            self.pathd = self.line + '\歌单下载\{}\歌曲\\'.format(purl2)
            # path = r'歌单下载\{}\歌词\\'.format(purl2)
            if os.path.isdir(self.pathc):
                pass
            else:
                os.makedirs(self.pathc)
            # path = r'歌单下载\{}\歌曲\\'.format(purl2)
            if os.path.isdir(self.pathd):
                pass
            else:
                os.makedirs(self.pathd)
            return purl2
        else:
            self.pathc = r'歌单下载\{}\歌词\\'.format(purl2)
            if os.path.isdir(self.pathc):
                pass
            else:
                os.makedirs(self.pathc)
            self.pathd = r'歌单下载\{}\歌曲\\'.format(purl2)
            if os.path.isdir(self.pathd):
                pass
            else:
                os.makedirs(self.pathd)
            return purl2

    def get_lyric(self,song_id):
        self.lrc_url = 'http://music.163.com/api/song/lyric?id=' + str(song_id) + '&lv=1&kv=1&tv=-1'
        self.html = self.get_html(self.lrc_url)
        j = json.loads(self.html)
        try:  # 部分歌曲没有歌词，这里引入一个异常
            lrc = j['lrc']['lyric']
            pat = re.compile(r'\[.*\]')
            lrc = re.sub(pat, "", lrc)
            lrc.strip()
            return lrc
        except KeyError as e:
            lrc = 0
            pass
            return lrc
    def write_lyric(self, song_name, lyric):
        html = self.get_html(self.start_url)
        singer_name3 = self.get_singer_info2(html)
        if lyric == 0:
            MyApp.text.insert(END, '这首没有歌词：{}'.format(song_name))
            MyApp.text.see(END)
            MyApp.text.update()
            pass
        else:
            path2 = r'log.txt'
            if os.path.exists(path2):
                with open('log.txt', 'r', encoding='utf-8') as f:
                    self.line = f.readline()
                if os.path.exists(
                    self.line +
                    '\歌单下载\{}\歌词'.format(singer_name3) +
                        '\{}.txt'.format(song_name)):
                    MyApp.text.insert(END, '歌词已存在：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    pass
                else:
                    MyApp.text.insert(END, '正在下载歌词：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    with open(self.line + '\歌单下载\{}\歌词'.format(singer_name3) + '\{}.txt'.format(song_name), 'a', encoding='utf-8') as fp:
                        fp.write(lyric)
            else:
                if os.path.exists(
                    '歌单下载\{}\歌词'.format(singer_name3) +
                        '\{}.txt'.format(song_name)):
                    MyApp.text.insert(END, '歌词已存在：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    pass
                else:
                    MyApp.text.insert(END, '正在下载歌词：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    with open('歌单下载\{}\歌词'.format(singer_name3) + '\{}.txt'.format(song_name), 'a', encoding='utf-8') as fp:
                        fp.write(lyric)
    def downloadsong(self,song_name, song_id):
        self.singer_url = 'https://music.163.com/song/media/outer/url?id={}.mp3'.format(song_id)
        html = self.get_html(self.start_url)
        singer_name3=self.get_singer_info2(html)
        self.r = requests.get(self.singer_url)
        hh = self.r.url
        if hh == 'http://music.163.com/404':
            MyApp.text.insert(END,'版权问题，无法下载：{}'.format(song_name))
            MyApp.text.see(END)
            MyApp.text.update()
        else:
            path2 = r'log.txt'
            if os.path.exists(path2):
                with open('log.txt', 'r', encoding='utf-8') as f:
                    self.line = f.readline()
                if os.path.exists(
                    self.line +
                    '\歌单下载\{}\歌曲'.format(singer_name3) +
                        '\{}.mp3'.format(song_name)):
                    MyApp.text.insert(END, '歌曲已存在：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    pass
                else:
                    MyApp.text.insert(END, '正在下载歌曲：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    urllib.request.urlretrieve(
                        self.singer_url,
                        self.line +
                        '\歌单下载\{}\歌曲'.format(singer_name3) +
                        '\{}.mp3'.format(song_name))
            else:
                if os.path.exists(
                    '歌单下载\{}\歌曲'.format(singer_name3) +
                        '\{}.mp3'.format(song_name)):
                    MyApp.text.insert(END, '歌曲已存在：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    pass
                else:
                    MyApp.text.insert(END, '正在下载歌曲：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    urllib.request.urlretrieve(
                        self.singer_url,
                        '歌单下载\{}\歌曲'.format(singer_name3) +
                        '\{}.mp3'.format(song_name))
    def stop(self):
         self.isRunning=True
class Pause(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        MyApp.text.insert(END, "123")
        MyApp.text.see(END)
        MyApp.text.update()

def button1_download():
      my_ftp = THread1()
      my_ftp.start()
def button2_download():
      my_ftp2 = THread2()
      my_ftp2.start()
def button3_download():
       my_ftp = THread3()
       my_ftp.start()
def button4_pause():
    t3 = Pause()
    t3.start()
if __name__ == '__main__':
    app=MyApp()
    section = section()
    menu = Menu(app, tearoff=0)
    menu.add_command(label="复制", command=section.onCopy)
    menu.add_separator()
    menu.add_command(label="粘贴", command=section.onPaste)
    menu.add_separator()
    menu.add_command(label="剪切", command=section.onCut)
    def popupmenu(event):
        menu.post(event.x_root, event.y_root)

    MyApp.entry.bind("<Button-3>", popupmenu)
    app.mainloop()