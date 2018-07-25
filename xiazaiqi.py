#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time   : 2018/7/14 0014 16:43
# @Author : wangyulin
# @File   : 网易下载器升级版.py
from tkinter import *
import psutil
from tkinter import ttk
from urllib.request import urlretrieve
from tkinter import messagebox
import urllib,os,re,urllib.request,requests,json,time,threading
from bs4 import BeautifulSoup
class MyApp(Tk):
    def __init__(self):
        super().__init__()
        self.wm_title('网易单曲音乐下载 BY wangyulin')
        sw = self.winfo_screenwidth()
        # 得到屏幕宽度
        sh = self.winfo_screenheight()
        # 得到屏幕高度
        ww = 550
        wh = 415
        # 窗口宽高为100
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        self.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
        self.resizable(width=False, height=False)  # 设置不可改变窗口大小
        self.attributes("-alpha", 1)  # 背景虚化
        self["bg"] = "white"  # 设置窗口的背景颜色
        self.protocol('WM_DELETE_WINDOW', self.closewindow)  # 绑定窗口退出事件
        self.setupUI()

    def closewindow(self):
        messagebox.showinfo(title="伤心o(╥﹏╥)o", message="你不想下载音乐吗( >﹏<。)～呜呜呜…… ")
        return

    def closequit(self):
        messagebox.showinfo(title='撒娇', message="再考虑一下呗o(￣ヘ￣o＃) ")
        return

    def chouju(self):
        messagebox.showinfo("o(` · ~ · ′。)o ", "真的不要我了吗<( ￣^￣)(θ(θ☆( >_< ")
        return
    def quit(self):
        quit1 = Toplevel(self)
        ww=300
        wh=100
        sw = self.winfo_screenwidth()
        # 得到屏幕宽度
        sh = self.winfo_screenheight()
        # 得到屏幕高度
        x1=(sw-ww)/2
        y1=(sw-sh)/2
        quit1.geometry("%dx%d+%d+%d" %(ww,wh,x1,y1-222/2))
        quit1.title("嘤嘤嘤<(－︿－)> ")
        label1 = Label(quit1, text="再考虑一下呗 ", font=("微软雅黑", 16))
        label1.grid(row=0, column=1)
        bun1 = Button(quit1, text="好的", width=10, height=2, command=quit1.destroy)
        bun1.grid(row=1, column=0, stick=W)
        bun2 = Button(quit1, text="丑拒", width=10, height=2, command=self.chouju)
        bun2.grid(row=1, column=2, sticky=E)
        quit1.protocol('WM_DELETE_WINDOW', self.closequit)
        quit1.wm_attributes('-topmost', 1)
        quit1.mainloop()

    def qingkong(self):
        MyApp.text.delete('0', 'end')
    def dakai(self):
        path = os.path.abspath(os.curdir)
        os.system('start explorer ' + path)  # c:为要打开c盘，也
    def inputclear(self):
        MyApp.entry.delete('0', 'end')#清除文本框内容
    def setupUI(self):  #设置根窗口的UI
        lable = Label(self, text='输入网易云链接或ID', font=('楷体', 20))
        lable.grid(row=0, column=0)
        lable = Label(self, text='输入网易云链接或ID', font=('楷体', 20))
        lable.grid(row=0, column=0)
        MyApp.url = StringVar()  # 这即是输入框中的内容
        # url.set('')  # 通过var.get()/var.set() 来 获取/设置var的值
        MyApp.entry=Entry(self, textvariable=MyApp.url, font=('微软雅黑', 15), width=23)
        MyApp.entry.grid(row=0, column=1)
        MyApp.text = Listbox(self, font=('微软雅黑', 15), width=45, height=10)
        MyApp.text.grid(row=1, columnspan=2)
        button = Button(self, text='单曲下载', font=('微软雅黑', 15),command=button1_download)
        button.place(x=0, y=316.5, width=103, height=45)
        button = Button(self, text='歌手下载', font=('微软雅黑', 15),command=button2_download)
        button.place(x=140, y=316.5, width=103, height=45)
        button = Button(self, text='打开文件', font=('微软雅黑', 15),command=self.dakai)
        button.place(x=140, y=365, width=103, height=45)
        button = Button(self, text='歌单下载', font=('微软雅黑', 15),command=button3_download)
        button.place(x=300, y=316.5, width=103, height=45)
        button = Button(self, text='清除链接', font=('微软雅黑', 15),command=self.inputclear)
        button.place(x=300, y=365, width=103, height=45)
        button = Button(self, text='残忍退出', font=('微软雅黑', 15),command=self.quit)
        button.place(x=447, y=316.5, width=103, height=45)
        button = Button(self, text='清空列表', font=('微软雅黑', 15),command=self.qingkong)
        button.place(x=0, y=365, width=103, height=45)
        button = Button(self, text='强制退出', font=('微软雅黑', 15), command=self.destroy)
        button.place(x=447, y=365, width=103, height=45)
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
class THread1(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.url1=MyApp.entry.get()  #
        self.singer_id = self.url1.split('=')[-1]
        self.start_url = 'https://music.163.com/song?id={}'.format(self.singer_id)
        self.html = self.get_html(self.start_url)
        self.song_name = self.get_song_name(self.html)
    def run(self):
        path = r'单曲下载\歌词\\'
        if os.path.isdir(path):
            pass
        else:
            os.makedirs(path)
        path = r'单曲下载\歌曲\\'
        if os.path.isdir(path):
            pass
        else:
            os.makedirs(path)
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
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'}
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
    def write_lyric(self,song_name, lyric):
        if lyric == 0:
            MyApp.text.insert(END,'这首没有歌词:{}'.format(song_name))
            MyApp.text.see(END)
            MyApp.text.update()
            pass
        else:
          if os.path.exists('单曲下载\歌词\{}.txt'.format(song_name)):
                MyApp.text.insert(END,'歌词已存在：{}'.format(song_name))
                MyApp.text.see(END)
                MyApp.text.update()
                pass
          else:
            MyApp.text.insert(END,'正在下载歌词：{}'.format(song_name))
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
            if os.path.exists('单曲下载\歌曲\{}.mp3'.format(song_name)):
                MyApp.text.insert(END,'歌曲已存在：{}'.format(song_name))
                MyApp.text.see(END)
                MyApp.text.update()
                pass
            else:
              MyApp.text.insert(END,'正在下载歌曲：{}'.format(song_name))
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
            for self.singer_info in self.get_information:
                lyric = self.get_lyric(self.singer_info[1])
                self.write_lyric(self.singer_info[0], lyric)
                self.downloadsong(self.singer_info[0], self.singer_info[1])
            MyApp.text.insert(END, '所有任务已经下载完毕')
            MyApp.text.see(END)
            MyApp.text.update()
    def get_html(self,url):
        self.header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'}
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
        path = r'歌手下载\{}\歌词\\'.format(purl2)
        if os.path.isdir(path):
            pass
        else:
            os.makedirs(path)
        path = r'歌手下载\{}\歌曲\\'.format(purl2)
        if os.path.isdir(path):
            pass
        else:
            os.makedirs(path)
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
    def write_lyric(self,song_name, lyric):
        html = self.get_html(self.start_url)
        singer_name3 = self.get_singer_info2(html)
        if lyric == 0:
            MyApp.text.insert(END,'这首没有歌词：{}'.format(song_name))
            MyApp.text.see(END)
            MyApp.text.update()
            pass
        else:
          if os.path.exists('歌手下载\{}\歌词'.format(singer_name3) + '\{}.txt'.format(song_name)):
                MyApp.text.insert(END, '歌词已存在：{}'.format(song_name))
                MyApp.text.see(END)
                MyApp.text.update()
                pass
          else:
            MyApp.text.insert(END,'正在下载歌词：{}'.format(song_name))
            MyApp.text.see(END)
            MyApp.text.update()
            with open('歌手下载\{}\歌词'.format(singer_name3)+'\{}.txt'.format(song_name), 'a', encoding='utf-8') as fp:
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
          if os.path.exists('歌手下载\{}\歌曲'.format(singer_name3) + '\{}.mp3'.format(song_name)):
                MyApp.text.insert(END, '歌曲已存在：{}'.format(song_name))
                MyApp.text.see(END)
                MyApp.text.update()
                pass
          else:
            MyApp.text.insert(END,'正在下载歌曲：{}'.format(song_name))
            MyApp.text.see(END)
            MyApp.text.update()
            urllib.request.urlretrieve(self.singer_url, '歌手下载\{}\歌曲'.format(singer_name3)+'\{}.mp3'.format(song_name))
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
        self.zanting()
        self.r = requests.get(self.start_url)
        self.hh = self.r.url
        if self.hh == 'https://music.163.com/404':
            MyApp.text.insert(END,'对不起，列表歌单出错')
        else:
            for self.singer_info in self.get_information:
                lyric = self.get_lyric(self.singer_info[1])
                self.write_lyric(self.singer_info[0], lyric)
                self.downloadsong(self.singer_info[0], self.singer_info[1])
            MyApp.text.insert(END, '所有任务已经下载完毕')
            MyApp.text.see(END)
            MyApp.text.update()
    def get_html(self,url):
        self.header = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 UBrowser/6.1.2107.204 Safari/537.36'}
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
        path = r'歌单下载\{}\歌词\\'.format(purl2)
        if os.path.isdir(path):
            pass
        else:
            os.makedirs(path)
        path = r'歌单下载\{}\歌曲\\'.format(purl2)
        if os.path.isdir(path):
            pass
        else:
            os.makedirs(path)
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
    def write_lyric(self,song_name, lyric):
        html = self.get_html(self.start_url)
        singer_name3 = self.get_singer_info2(html)
        if lyric == 0:
            MyApp.text.insert(END,'这首没有歌词：{}'.format(song_name))
            MyApp.text.see(END)
            MyApp.text.update()
            pass
        else:

            if os.path.exists('歌单下载\{}\歌词'.format(singer_name3)+'\{}.txt'.format(song_name)):
                MyApp.text.insert(END, '歌词已存在：{}'.format(song_name))
                MyApp.text.see(END)
                MyApp.text.update()
                pass
            else:
              MyApp.text.insert(END,'正在下载歌词：{}'.format(song_name))
              MyApp.text.see(END)
              MyApp.text.update()
              with open('歌单下载\{}\歌词'.format(singer_name3)+'\{}.txt'.format(song_name), 'a', encoding='utf-8') as fp:
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
         if os.path.exists('歌单下载\{}\歌曲'.format(singer_name3) + '\{}.mp3'.format(song_name)):
             MyApp.text.insert(END,'歌曲已存在：{}'.format(song_name))
             MyApp.text.see(END)
             MyApp.text.update()
             pass
         else:
           MyApp.text.insert(END,'正在下载歌曲：{}'.format(song_name))
           MyApp.text.see(END)
           MyApp.text.update()
           urllib.request.urlretrieve(self.singer_url, '歌单下载\{}\歌曲'.format(singer_name3)+'\{}.mp3'.format(song_name))
    def stop(self):
         self.isRunning=True
def button1_download():
      my_ftp = THread1()
      my_ftp.start()
def button2_download():
      my_ftp2 = THread2()
      my_ftp2.start()
def button3_download():
       my_ftp = THread3()
       my_ftp.start()
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