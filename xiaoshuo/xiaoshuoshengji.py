#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time   : 2018/7/29 0029 20:25
# @Author : wangyulin
# @File   : 爬取小说.py
import requests,time
from bs4 import BeautifulSoup
from tkinter import *
from lxml import etree
import os,re,threading
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
        x = (sw - ww) / 2
        y = (sh - wh) / 2
        # self.iconbitmap('icons\\format.ico')
        self.geometry("%dx%d+%d+%d" % (ww, wh, x, y))
        self.resizable(width=False, height=False)  # 设置不可改变窗口大小
        self.attributes("-alpha", 1)  # 背景虚化
        self["bg"] = "white"  # 设置窗口的背景颜色
        self.protocol('WM_DELETE_WINDOW', self.destroy)  # 绑定窗口退出事件
        self.setupUI()
    def dakai(self):
        path = os.path.abspath(os.curdir)
        os.system('start explorer ' + path)  # c:为要打开c盘，也
    def qingkong(self):
        MYapp.entry.delete('0', 'end')#清除文本框内容
    def setupUI(self):  # 设置根窗口的UI
        lable = Label(self, text='请输入小说网页地址', font=('楷体', 20))
        lable.grid(row=0, column=0)

        MYapp.url = StringVar()  # 这即是输入框中的内容
        MYapp.entry=Entry(self, textvariable=MYapp.url, font=('微软雅黑', 15), width=23)
        MYapp.entry.grid(row=0, column=1)
        MYapp.text = Listbox(self, font=('微软雅黑', 15), width=45, height=10)
        MYapp.text.grid(row=1, columnspan=2)
        button = Button(self, text='笔趣阁小说', font=('微软雅黑', 15),command=download2)
        button.grid(row=2,columnspan=2,sticky=S+W)
        button = Button(self, text='海岸线小说', font=('微软雅黑', 15), command=download)
        button.grid(row=2, columnspan=2)
        button = Button(self, text='清空地址栏', font=('微软雅黑', 15),command=self.qingkong)
        button.grid(row=3, columnspan=2,sticky=S+W)
        button = Button(self, text='退出程序', font=('微软雅黑', 15), command=self.destroy)
        button.grid(row=3, columnspan=2,sticky=N+E)
        button = Button(self, text='打开文件', font=('微软雅黑', 15), command=self.dakai)
        button.grid(row=2, columnspan=2, sticky=N + E)
class xiazai(threading.Thread):
    global x
    def __init__(self):
        threading.Thread.__init__(self)
        self.url1 = MYapp.entry.get()
        self.xiaoshuo_id = self.url1.split('info/')[-1]
        if self.xiaoshuo_id==self.url1:
             self.new_url=self.xiaoshuo_id
        else:
          self.id=self.xiaoshuo_id.replace('.htm','')
          self.new_url='https://www.haxds.com/files/article/html/{}/index.html'.format(self.id)
    def run(self):
        self.new_url3=self.new_url.split('html')[0]
        if self.new_url3!='https://www.haxds.com/files/article/':
           MYapp.text.insert(END,'请输入正确地址')
           MYapp.text.see(END)
           MYapp.text.update()
        else :
         x = 0
         self.url_2 = self.get_url(self.new_url)
         for i in self.url_2[0]:
            test=self.download(i)
            c=str(x)
            a=c+test[0]
            b=test[1]
            self.write(a,b)
            x+=1
         self.hebing()
         MYapp.text.insert(END,'合并成功')
         MYapp.text.see(END)
         MYapp.text.update()
    def get_url(self,url1):
      header = {'Accept':     '*/*', 'Accept-Language': 'en-US,en;q=0.8', 'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
               'Connection': 'keep-alive', 'Referer': 'https://www.readnovel.com/'}

      self.html=requests.get(url1,headers=header).text
      req1='<h1>(.*?)</h1>'
      book_name=re.findall(req1,self.html)
      req2='target="_blank">(.*?)</a>'

      author_name=re.findall(req2,self.html)
      for a in author_name:
         self.authorname=a
      for i in book_name:
         self.newname=i
      self.newwname=self.newname+'---'+self.authorname
      path = r'小说下载\海岸线小说\{}\\'.format(self.newwname)
      if os.path.isdir(path):
          pass
      else:
          os.makedirs(path)
      req = '<dd><a href="(.*?)"'
      self.purl = re.findall(req, self.html)
      self.newpurl1=[]
      for i in self.purl:
          self.newpurl='https://www.haxds.com'+i
          self.newpurl1.append(self.newpurl)
      return self.newpurl1,self.newwname
    def download(self,url):
      header = {'Accept':     '*/*', 'Accept-Language': 'en-US,en;q=0.8', 'Cache-Control': 'max-age=0',
              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
              'Connection': 'keep-alive', 'Referer': 'https://www.readnovel.com/'}
      html1 = requests.get(url,headers=header).text
      req = '<h1>(.*?)</h1>'
      biaoti=re.findall(req, html1)
      self.biaoti2=biaoti[0]
      MYapp.text.insert(END,'正在下载章节：{}'.format(self.biaoti2))
      MYapp.text.see(END)
      MYapp.text.update()
      req1 = '<div id="BookText">(.*?)</div>'
      self.title=re.findall(req1,html1,re.S)
      return self.biaoti2,self.title
    def write(self,name,title1):
       # with open('小说下载\{}'.format(self.url_2[1]) + '\{}.txt'.format(name), 'a', encoding='utf-8') as ff:
       #     ff.write(name)
       for i in title1:
         par=i.replace('<br /><br /> ','')
         paragraph1=par.replace('<br>','\n')
         # paragraph2 = paragraph1.replace("　　", '\n')
         if os.path.exists('小说下载\海岸线小说\{}'.format(self.url_2[1]) + '\{}.txt'.format(name)):
             MYapp.text.insert(END, '已存在：{}'.format(name))
             MYapp.text.see(END)
             MYapp.text.update()
             pass
         else:
           with open('小说下载\海岸线小说\{}'.format(self.url_2[1]) + '\{}.txt'.format(name), 'a', encoding='utf-8') as fp:
            # fp.write('\n')
             fp.write(paragraph1)
             time.sleep(0.08)
    def hebing(self):
        filedir = r'小说下载\海岸线小说\{}\\'.format(self.newwname)
        # 获取当前文件夹中的文件名称列表
        filenames = os.listdir(filedir)
        # 打开当前目录下的result.txt文件，如果没有则创建
        f = open('小说下载\海岸线小说\{}.txt'.format(self.newwname), 'w', encoding='utf-8')
        # 先遍历文件名
        for filename in filenames:
            filepath = filedir + '/' + filename
            # 遍历单个文件，读取行数
            for line in open(filepath, encoding='utf-8'):
                f.writelines(line)
        f.close()
    def stop(self):
         self.isRunning=True
class xiazai2(threading.Thread):
    global x
    def __init__(self):
        threading.Thread.__init__(self)
        self.url1 = MYapp.entry.get()
        self.xiaoshuo_id = self.url1.split('cc/')[-1]
        self.id=self.xiaoshuo_id.replace('/','')
        self.new_url='https://www.biquge5200.cc/{}/'.format(self.id)
    def run(self):
        if self.new_url == 'https://www.biquge5200.cc//':
                MYapp.text.insert(END, '请输入正确链接')
                MYapp.text.see(END)
                MYapp.text.update()
        else:
          x = 0
          self.url_2 = self.get_url(self.url1)
          for i in self.url_2[0]:
            test=self.download(i)
            c=str(x)
            a=c+test[0]
            b=test[1]
            self.write(a,b)
            x+=1
        self.hebing()
        MYapp.text.insert(END,'合并成功')
        MYapp.text.see(END)
        MYapp.text.update()
    def get_url(self,url1):
      header = {'Accept':     '*/*', 'Accept-Language': 'en-US,en;q=0.8', 'Cache-Control': 'max-age=0',
               'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
               'Connection': 'keep-alive', 'Referer': 'https://www.readnovel.com/'}

      html=requests.get(url1,headers=header).text
      req1='book_name" content="(.*?)"'
      book_name=re.findall(req1,html)
      req2='author" content="(.*?)"'
      author_name=re.findall(req2,html)
      for a in author_name:
         self.authorname=a
      for i in book_name:
         self.newname=i
      self.newwname=self.newname+'---'+self.authorname
      path = r'小说下载\笔趣阁小说\{}\\'.format(self.newwname)
      if os.path.isdir(path):
          pass
      else:
          os.makedirs(path)
      req = '<dd><a href="(.*?)"'
      self.purl = re.findall(req, html)
      return self.purl,self.newwname
    def download(self,url):
      header = {'Accept':     '*/*', 'Accept-Language': 'en-US,en;q=0.8', 'Cache-Control': 'max-age=0',
              'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
              'Connection': 'keep-alive', 'Referer': 'https://www.readnovel.com/'}
      html1 = requests.get(url,headers=header).text
      req = '<h1>(.*?)</h1>'
      biaoti=re.findall(req, html1)
      self.biaoti2=biaoti[0]
      MYapp.text.insert(END,'正在下载章节：{}'.format(self.biaoti2))
      MYapp.text.see(END)
      MYapp.text.update()
      req1 = '<div id="content">(.*?)</div>'
      self.title=re.findall(req1,html1,re.S)
      return self.biaoti2,self.title
    def write(self,name,title1):
       if os.path.exists('小说下载\笔趣阁小说\{}'.format(self.url_2[1]) + '\{}.txt'.format(name)):
            MYapp.text.insert(END, '已存在：{}'.format(name))
            MYapp.text.see(END)
            MYapp.text.update()
            pass
       else:
         with open('小说下载\笔趣阁小说\{}'.format(self.url_2[1]) + '\{}.txt'.format(name), 'a', encoding='utf-8') as ff:
            ff.write(name+'\n')
         for i in title1:
            par = i.replace('<p>', '')
            paragraph1 = par.replace('</p>', '\n')
            with open('小说下载\笔趣阁小说\{}'.format(self.url_2[1]) + '\{}.txt'.format(name), 'a', encoding='utf-8') as fp:
               fp.write(paragraph1)
               time.sleep(0.08)
    def hebing(self):
        filedir = r'小说下载\笔趣阁小说\{}\\'.format(self.newwname)
        # 获取当前文件夹中的文件名称列表
        filenames = os.listdir(filedir)
        # 打开当前目录下的result.txt文件，如果没有则创建

        f = open('小说下载\笔趣阁小说\{}.txt'.format(self.newwname), 'w', encoding='utf-8')
        # 先遍历文件名
        for filename in filenames:
            filepath = filedir + '/' + filename
            # 遍历单个文件，读取行数
            for line in open(filepath, encoding='utf-8'):
                f.writelines(line)
        f.close()
    def stop(self):
         self.isRunning=True
def download():
    test=xiazai()
    test.start()
def download2():
        test = xiazai2()
        test.start()
if __name__ == '__main__':
    app=MYapp()
    app.mainloop()