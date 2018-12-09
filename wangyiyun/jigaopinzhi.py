#!/usr/bin/python
# -*- coding:utf-8 -*-
# @Time   : 2018/7/14 0014 16:43
# @Author : wangyulin
# @File   : 网易下载器升级版.py
from tkinter import *
from Crypto.Cipher import AES
from multiprocessing import Pool
from multiprocessing.dummy import Pool
from tkinter.filedialog import askdirectory
from http import cookiejar
from tkinter import ttk
from urllib.request import urlretrieve
from tkinter import messagebox
from bs4 import BeautifulSoup
import urllib
import os
import re
import urllib.request
import requests
import json
import time
import threading
import base64
import binascii
import click
headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'music.163.com',
    'Referer': 'http://music.163.com/search/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
}
# 下载时header
download_headers = {
    'Accept-Encoding': 'identity;q=1, *;q=0',
    'DNT': '1',
    'Range': 'bytes=0-',
    'Referer': 'http://music.163.com/',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
}
# 网易云音乐api 的uri
apis = {
    'song_detail': '/weapi/v3/song/detail',
    'song_url': '/weapi/song/enhance/player/url',
    'play_detail': '/api/playlist/detail?id=%s',
    'album': '/weapi/v1/album/%s',
    'artist': '/weapi/v1/artist/%s',
    'artist_album': '/weapi/artist/albums/%s',
    'djradio': '/weapi/dj/program/byradio',
    'dj': '/weapi/dj/program/detail',
}

ss = requests.session()
ss.headers.update(headers)


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
#
    def setupui(self):
        # 设置窗口UI
        # StringVar()  # 这即是输入框中的内容
        # url.set('')  # 通过var.get()/var.set() 来 获取/设置var的值
        lable = Label(self, text='输入网易云链接或ID', font=('楷体', 20))
        lable.grid(row=0, column=0)
        # lable = Label(self, text='输入网易云链接或ID', font=('楷体', 20))
        # lable.grid(row=0, column=0)
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


class Section:

    def onpaste(self):
        try:
            self.text = app.clipboard_get()
        except TclError:
            pass
        MyApp.url.set(str(self.text))

    def oncopy(self):
        self.text = MyApp.entry.get()
        app.clipboard_append(self.text)

    def oncut(self):
        self.onCopy()
        try:
            MyApp.entry.delete('sel.first', 'sel.last')
        except TclError:
            pass


class Encrypyed:
    # 解密算法  登录加密算法, 基于https://github.com/stkevintan/nw_musicbox脚本实现
    def __init__(self):
        self.modulus = '00e0b509f6259df8642dbc35662901477df22677ec' \
                       '152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e' \
                       '417629ec4ee341f56135fccf695280104e0312ecbda92557c938' \
                       '70114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cf' \
                       'e4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7'
        self.nonce = '0CoJUm6Qyw8W8jud'
        self.pub_key = '010001'

    def encrypted_request(self, text):
        text = json.dumps(text)
        sec_key = self.create_secret_key(16)
        enc_text = self.aes_encrypt(
            self.aes_encrypt(
                text,
                self.nonce),
            sec_key.decode('utf-8'))
        enc_sec_key = self.rsa_encrpt(sec_key, self.pub_key, self.modulus)
        data = {'params': enc_text, 'encSecKey': enc_sec_key}
        return data

    @staticmethod
    def aes_encrypt(text, secKey):
        pad = 16 - len(text) % 16
        text = text + chr(pad) * pad
        encryptor = AES.new(
            secKey.encode('utf-8'),
            AES.MODE_CBC,
            b'0102030405060708')
        ciphertext = encryptor.encrypt(text.encode('utf-8'))
        ciphertext = base64.b64encode(ciphertext).decode('utf-8')
        return ciphertext

    @staticmethod
    def rsa_encrpt(text, pubKey, modulus):
        text = text[::-1]
        rs = pow(int(binascii.hexlify(text), 16),
                 int(pubKey, 16), int(modulus, 16))
        return format(rs, 'x').zfill(256)

    @staticmethod
    def create_secret_key(size):
        return binascii.hexlify(os.urandom(size))[:16]


class Crawler:
    # 网易云爬取API
    def __init__(self, timeout=60, cookie_path='.'):
        self.song_infos = []
        self.headers = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'http://music.163.com/search/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/63.0.3239.132 Safari/537.36'}
        self.session = requests.Session()
        self.session.headers.update(self.headers)
        self.session.cookies = cookiejar.LWPCookieJar(cookie_path)
        self.download_session = requests.Session()
        self.timeout = timeout
        self.ep = Encrypyed()

    def post_request(self, uri, params):
        # Post请求  return: 字典
        data = self.ep.encrypted_request(params)
        resp = ss.post(
            'http://music.163.com/%s' %
            uri, data=data, timeout=self.timeout)
        # resp = self.session.post(url, data=data, timeout=self.timeout)
        result = resp.json()

        if result['code'] != 200:
            click.echo('post_request error')
        else:
            return result

    def get_durls(self, songs):
        params = {
            'ids': list(
                s["id"] for s in songs),
            'br': '320000',
            'csrf_token': ''}
        result = self.post_request(apis['song_url'], params)
        for s in result['data']:
            if result['code'] == 200:
                return [str(s["id"]), s["url"]]


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


class THread_1(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.url1 = MyApp.entry.get()

    def run(self):
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            self.patha = self.line + '\单曲下载'
            if os.path.isdir(self.patha):
                pass
            else:
                os.makedirs(self.patha)
        else:
            self.patha = r'单曲下载\\'
            if os.path.isdir(self.patha):
                pass
            else:
                os.makedirs(self.patha)

        if self.url1 == '':
            MyApp.text.insert(END, '对不起，请输入ID或链接')
            MyApp.text.see(END)
            MyApp.text.update()
            return
        else:
            self.singer_id = self.url1.split('=')[-1]
            self.start_url = 'https://music.163.com/song?id={}'.format(
                self.singer_id)

            self.r = requests.get(self.start_url)
            hh = self.r.url
            if hh == 'https://music.163.com/404':
                MyApp.text.insert(END, '对不起，歌曲出错')
                MyApp.text.see(END)
                MyApp.text.update()
                return
            else:
                self.html = self.get_html(self.start_url)

                self.song_name = self.get_song_name(self.html)
                lyric = self.get_lyric(self.singer_id)
                self.write_lyric(self.song_name, lyric)

                self.download_song(self.song_name, self.singer_id)
                MyApp.text.insert(END, '任务已经完成(*￣▽￣)y ')
                MyApp.text.see(END)
                MyApp.text.update()

    def get_html(self, url):
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
        except BaseException:
            MyApp.text.insert(END, "解析错误")
            MyApp.text.see(END)
            MyApp.text.update()
            pass

    def get_song_name(self, html):
        self.soup = BeautifulSoup(html, "lxml")
        self.soup1 = self.soup.find('title')
        for i in self.soup1:
            self.song_name = i.split('-')[0]
            rstr = r"[\/\\\:\*\?\"\<\>\|\？]"  # '/ \ : * ? " < > | ？'
            self.newName = re.sub(rstr, " ", self.song_name)  # 替换为空格
            return self.newName

    def get_lyric(self, song_id):
        self.lrc_url = 'http://music.163.com/api/song/lyric?id=' + \
            str(song_id) + '&lv=1&kv=1&tv=-1'
        self.html1 = self.get_html(self.lrc_url)
        j = json.loads(self.html1)
        try:  # 部分歌曲没有歌词，这里引入一个异常
            lrc = j['lrc']['lyric']
            pat = re.compile(r'\[.*\]')
            lrc = re.sub(pat, "", lrc)
            lrc.strip()
            return lrc
        except KeyError:
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
                        self.line + '\单曲下载\\{}.txt'.format(song_name)):
                    MyApp.text.insert(END, '歌词已存在：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    pass
                else:
                    MyApp.text.insert(END, '正在下载歌词：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    with open(self.line + '\单曲下载\\{}.txt'.format(song_name), 'a', encoding='utf-8') as fp:
                        fp.write(lyric)
            else:
                if os.path.exists('单曲下载\{}.txt'.format(song_name)):
                    MyApp.text.insert(END, '歌词已存在：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    pass
                else:
                    MyApp.text.insert(END, '正在下载歌词：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    with open('单曲下载\\{}.txt'.format(song_name), 'a', encoding='utf-8') as fp:
                        fp.write(lyric)

    def download_song(self, song_name, song_id):
        bit_rate = 320000
        # url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        # csrf = ''
        # params = {'ids': [song_id], 'br': bit_rate, 'csrf_token': csrf}
        ts = Crawler()
        # result = ts.post_request(url, params)
        # # 歌曲下载地址
        # song_url = result['data'][0]['url']
        params = {'c': str([{'id': song_id}]), 'ids': [
            song_id], 'br': bit_rate, 'csrf_token': ''}
        result = ts.post_request(apis['song_detail'], params)
        result2 = ts.get_durls(result['songs'])
        song_url = result2[1]
        if song_url is None:
            MyApp.text.insert(END, '版权问题，无法下载：{}'.format(song_name))
            MyApp.text.see(END)
            MyApp.text.update()
        else:
            path2 = r'log.txt'
            if os.path.exists(path2):
                with open('log.txt', 'r', encoding='utf-8') as f:
                    self.line = f.readline()
                if os.path.exists(
                        self.line + '\单曲下载\{}.mp3'.format(song_name)):
                    MyApp.text.insert(END, '歌曲已存在：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    pass
                else:
                    MyApp.text.insert(END, '正在下载歌曲：{}'.format(song_name))
                    urllib.request.urlretrieve(
                        song_url, self.line + '\单曲下载\\{}.mp3'.format(song_name))
            else:
                if os.path.exists('单曲下载\{}.mp3'.format(song_name)):
                    MyApp.text.insert(END, '歌曲已存在：{}'.format(song_name))
                    MyApp.text.see(END)
                    MyApp.text.update()
                    pass
                else:
                    MyApp.text.insert(END, '正在下载歌曲：{}'.format(song_name))
                    urllib.request.urlretrieve(
                        song_url, '单曲下载\\{}.mp3'.format(song_name))

    def stop(self):
        self.isRunning = True

class THread_2(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.url1 = MyApp.entry.get()  #

    def run(self):
        if self.url1 == '':
            MyApp.text.insert(END, '对不起，请输入正确ID或链接')
            MyApp.text.see(END)
            MyApp.text.update()
            pass
        else:
            self.singer_id = self.url1.split('=')[-1]
            self.start_url = 'https://music.163.com/artist?id={}'.format(
                self.singer_id)
            self.r = requests.get(self.start_url)
            self.hh = self.r.url
            if self.hh == 'https://music.163.com/404':
                MyApp.text.insert(END, '对不起，列表歌单出错')
                MyApp.text.see(END)
                MyApp.text.update()
            else:
                self.html = self.get_html(self.start_url)
                self.get_information = self.get_singer_info(self.html)
                MyApp.text.insert(END,
                                  '歌单中共有{}首歌曲需要下载'.format(len(self.get_information)))
                MyApp.text.see(END)
                MyApp.text.update()
                self.singe_IDI = []
                for i in self.get_information:
                    self.bb = i.split('/')[0]
                    self.aa = i.split('/')[1]
                    self.singe_IDI.append(self.aa)
                pool = Pool(35)
                pool.map(self.downloadsong, self.singe_IDI)
                MyApp.text.insert(END, '所有任务已经下载完毕')
                MyApp.text.see(END)
                MyApp.text.update()

    def get_html(self, url):
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
        except BaseException:
            MyApp.text.insert(END, "解析错误")
            MyApp.text.see(END)
            MyApp.text.update()
            pass

    def get_singer_info(self, html):
        self.soup = BeautifulSoup(html, "lxml")
        self.links = self.soup.find('ul', class_='f-hide').find_all('a')
        self.song_IDs = []
        x = 1
        for link in self.links:
            song_ID = str(x) + '/' + link.get('href').split('=')[-1]
            x += 1
            self.song_IDs.append(song_ID)

        return self.song_IDs

    def get_singer_info2(self, playlist):
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
            self.pathc = self.line + '\歌手下载\{}\\'.format(purl2)
            if os.path.isdir(self.pathc):
                pass
            else:
                os.makedirs(self.pathc)
            return purl2
        else:
            self.pathc = r'歌手下载\{}\\'.format(purl2)
            if os.path.isdir(self.pathc):
                pass
            else:
                os.makedirs(self.pathc)
            return purl2

    def get_lyric(self, song_id,song_name):
        self.lrc_url = 'http://music.163.com/api/song/lyric?id=' + \
            str(song_id) + '&lv=1&kv=1&tv=-1'
        self.html = self.get_html(self.lrc_url)
        j = json.loads(self.html)
        try:  # 部分歌曲没有歌词，这里引入一个异常
            lrc = j['lrc']['lyric']
            pat = re.compile(r'\[.*\]')
            lrc = re.sub(pat, "", lrc)
            lrc.strip()
            self.write_lyric(song_name,lrc)
        except KeyError:
            lrc = 0
            pass
            self.write_lyric(song_name, lrc)

    def write_lyric(self, song_name, lyric):
        html = self.get_html(self.start_url)
        singer_name3 = self.get_singer_info2(html)
        if lyric == 0:
            pass
        else:
            path2 = r'log.txt'
            if os.path.exists(path2):
                with open('log.txt', 'r', encoding='utf-8') as f:
                    self.line = f.readline()
                if os.path.exists(
                    self.line +
                    '\歌手下载\{}'.format(singer_name3) +
                        '\{}.txt'.format(song_name)):
                    pass
                else:
                    with open(self.line + '\歌手下载\{}'.format(singer_name3) + '\{}.txt'.format(song_name), 'a', encoding='utf-8') as fp:
                        fp.write(lyric)
            else:
                if os.path.exists(
                    '歌手下载\{}'.format(singer_name3) +
                        '\{}.txt'.format(song_name)):
                    pass
                else:
                    with open('歌手下载\{}'.format(singer_name3) + '\{}.txt'.format(song_name), 'a', encoding='utf-8') as fp:
                        fp.write(lyric)

    def downloadsong(self,song_id):
        url1='https://music.163.com/song?id='+song_id
        html = requests.get(url1, headers=headers, timeout=10).text
        req='"title": "(.*?)"'
        name=re.findall(req,html)
        newwname1 = []
        for result in name:
            rstr = r"[\/\\\:\*\?\"\<\>\|\？]"  # '/ \ : * ? " < > | ？'
            newName = re.sub(rstr, " ", result)  # 替换为空格
            newwname1.append(newName)
        bit_rate = 320000
        # url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        # csrf = ''
        # # params = {'ids': [song_id], 'br': bit_rate, 'csrf_token': csrf}
        ts = Crawler()
        params = {'c': str([{'id': song_id}]), 'ids': [
            song_id], 'br': bit_rate, 'csrf_token': ''}
        result = ts.post_request(apis['song_detail'], params)
        result2 = ts.get_durls(result['songs'])
        # # 歌曲下载地址
        # song_url = result['data'][0]['url']
        song_url = result2[1]
        html = self.get_html(self.start_url)
        singer_name3 = self.get_singer_info2(html)
        if song_url is None:
           return
        else:
            self.write(song_url,singer_name3,newwname1[0])
            self.get_lyric(song_id,newwname1[0])
    def write(self,song_url,singer_name3,newwname1):
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            if os.path.exists(
                self.line +
                '\歌手下载\{}'.format(singer_name3) +
                    '\{}.mp3'.format(newwname1)):
                MyApp.text.insert(END, '歌手已存在：{}'.format(newwname1))
                MyApp.text.see(END)
                MyApp.text.update()
                pass
            else:
                MyApp.text.insert(END, '正在下载歌曲：{}'.format(newwname1))
                MyApp.text.see(END)
                MyApp.text.update()
                urllib.request.urlretrieve(
                    song_url,
                    self.line +
                    '\歌手下载\{}'.format(singer_name3) +
                    '\{}.mp3'.format(newwname1))
        else:

            if os.path.exists(
                    '歌手下载\{}'.format(singer_name3) +
                    '\{}.mp3'.format(newwname1)):
                MyApp.text.insert(END, '歌曲已存在：{}'.format(newwname1))
                MyApp.text.see(END)
                MyApp.text.update()
                pass
            else:
                # ‘第{}'.format(song_num)+'首’
                MyApp.text.insert(END, '正在下载歌曲：{}'.format(newwname1))
                MyApp.text.see(END)
                MyApp.text.update()
                urllib.request.urlretrieve(
                    song_url,
                    '歌手下载\{}'.format(singer_name3) +
                    '\{}.mp3'.format(newwname1))

    def stop(self):
        self.isRunning = True

class THread_3(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.url1 = MyApp.entry.get()  #

    def run(self):
        if self.url1 == '':
            MyApp.text.insert(END, '对不起，请输入正确ID或链接')
            MyApp.text.see(END)
            MyApp.text.update()
            pass
        else:
            self.singer_id = self.url1.split('=')[-1]
            self.start_url = 'https://music.163.com/playlist?id={}'.format(
                self.singer_id)
            self.r = requests.get(self.start_url)
            self.hh = self.r.url
            if self.hh == 'https://music.163.com/404':
                MyApp.text.insert(END, '对不起，列表歌单出错')
                MyApp.text.see(END)
                MyApp.text.update()
            else:
                self.html = self.get_html(self.start_url)
                self.get_information = self.get_singer_info(self.html)
                MyApp.text.insert(END,
                                  '歌单中共有{}首歌曲需要下载'.format(len(self.get_information)))
                MyApp.text.see(END)
                MyApp.text.update()
                self.singe_IDI = []
                for i in self.get_information:
                    self.bb = i.split('/')[0]
                    self.aa = i.split('/')[1]
                    self.singe_IDI.append(self.aa)
                pool = Pool(35)
                pool.map(self.downloadsong, self.singe_IDI)
                MyApp.text.insert(END, '所有任务已经下载完毕')
                MyApp.text.see(END)
                MyApp.text.update()

    def get_html(self, url):
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
        except BaseException:
            MyApp.text.insert(END, "解析错误")
            MyApp.text.see(END)
            MyApp.text.update()
            pass

    def get_singer_info(self, html):
        self.soup = BeautifulSoup(html, "lxml")
        self.links = self.soup.find('ul', class_='f-hide').find_all('a')
        self.song_IDs = []
        x = 1
        for link in self.links:
            song_ID = str(x) + '/' + link.get('href').split('=')[-1]
            x += 1
            self.song_IDs.append(song_ID)

        return self.song_IDs

    def get_singer_info2(self, playlist):
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
            self.pathc = self.line + '\歌单下载\{}\\'.format(purl2)
            if os.path.isdir(self.pathc):
                pass
            else:
                os.makedirs(self.pathc)
            return purl2
        else:
            self.pathc = r'歌单下载\{}\\'.format(purl2)
            if os.path.isdir(self.pathc):
                pass
            else:
                os.makedirs(self.pathc)
            return purl2

    def get_lyric(self, song_id,song_name):
        self.lrc_url = 'http://music.163.com/api/song/lyric?id=' + \
            str(song_id) + '&lv=1&kv=1&tv=-1'
        self.html = self.get_html(self.lrc_url)
        j = json.loads(self.html)
        try:  # 部分歌曲没有歌词，这里引入一个异常
            lrc = j['lrc']['lyric']
            pat = re.compile(r'\[.*\]')
            lrc = re.sub(pat, "", lrc)
            lrc.strip()
            self.write_lyric(song_name,lrc)
        except KeyError:
            lrc = 0
            pass
            self.write_lyric(song_name, lrc)

    def write_lyric(self, song_name, lyric):
        html = self.get_html(self.start_url)
        singer_name3 = self.get_singer_info2(html)
        if lyric == 0:
            pass
        else:
            path2 = r'log.txt'
            if os.path.exists(path2):
                with open('log.txt', 'r', encoding='utf-8') as f:
                    self.line = f.readline()
                if os.path.exists(
                    self.line +
                    '\歌单下载\{}'.format(singer_name3) +
                        '\{}.txt'.format(song_name)):
                    pass
                else:
                    with open(self.line + '\歌单下载\{}'.format(singer_name3) + '\{}.txt'.format(song_name), 'a', encoding='utf-8') as fp:
                        fp.write(lyric)
            else:
                if os.path.exists(
                    '歌单下载\{}'.format(singer_name3) +
                        '\{}.txt'.format(song_name)):
                    pass
                else:
                    with open('歌单下载\{}'.format(singer_name3) + '\{}.txt'.format(song_name), 'a', encoding='utf-8') as fp:
                        fp.write(lyric)

    def downloadsong(self,song_id):
        url1='https://music.163.com/song?id='+song_id
        html = requests.get(url1, headers=headers, timeout=10).text
        req='"title": "(.*?)"'
        name=re.findall(req,html)
        newwname1 = []
        for result in name:
            rstr = r"[\/\\\:\*\?\"\<\>\|\？]"  # '/ \ : * ? " < > | ？'
            newName = re.sub(rstr, " ", result)  # 替换为空格
            newwname1.append(newName)
        bit_rate = 320000
        # url = 'http://music.163.com/weapi/song/enhance/player/url?csrf_token='
        # csrf = ''
        # # params = {'ids': [song_id], 'br': bit_rate, 'csrf_token': csrf}
        ts = Crawler()
        params = {'c': str([{'id': song_id}]), 'ids': [
            song_id], 'br': bit_rate, 'csrf_token': ''}
        result = ts.post_request(apis['song_detail'], params)
        result2 = ts.get_durls(result['songs'])
        # # 歌曲下载地址
        # song_url = result['data'][0]['url']
        song_url = result2[1]
        html = self.get_html(self.start_url)
        singer_name3 = self.get_singer_info2(html)
        if song_url is None:
           return
        else:
            self.write(song_url,singer_name3,newwname1[0])
            self.get_lyric(song_id,newwname1[0])
    def write(self,song_url,singer_name3,newwname1):
        path2 = r'log.txt'
        if os.path.exists(path2):
            with open('log.txt', 'r', encoding='utf-8') as f:
                self.line = f.readline()
            if os.path.exists(
                self.line +
                '\歌单下载\{}'.format(singer_name3) +
                    '\{}.mp3'.format(newwname1)):
                MyApp.text.insert(END, '歌曲已存在：{}'.format(newwname1))
                MyApp.text.see(END)
                MyApp.text.update()
                pass
            else:
                MyApp.text.insert(END, '正在下载歌曲：{}'.format(newwname1))
                MyApp.text.see(END)
                MyApp.text.update()
                urllib.request.urlretrieve(
                    song_url,
                    self.line +
                    '\歌单下载\{}'.format(singer_name3) +
                    '\{}.mp3'.format(newwname1))
        else:

            if os.path.exists(
                    '歌单下载\{}'.format(singer_name3) +
                    '\{}.mp3'.format(newwname1)):
                MyApp.text.insert(END, '歌曲已存在：{}'.format(newwname1))
                MyApp.text.see(END)
                MyApp.text.update()
                pass
            else:
                # ‘第{}'.format(song_num)+'首’
                MyApp.text.insert(END, '正在下载歌曲：{}'.format(newwname1))
                MyApp.text.see(END)
                MyApp.text.update()
                urllib.request.urlretrieve(
                    song_url,
                    '歌单下载\{}'.format(singer_name3) +
                    '\{}.mp3'.format(newwname1))

    def stop(self):
        self.isRunning = True


class Pause(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        MyApp.text.insert(END, "123")
        MyApp.text.see(END)
        MyApp.text.update()


def button1_download():
    my_ftp = THread_1()
    my_ftp.setDaemon(True)
    my_ftp.start()


def button2_download():
    my_ftp2 = THread_2()
    my_ftp2.setDaemon(True)
    my_ftp2.start()


def button3_download():
    my_ftp = THread_3()
    my_ftp.setDaemon(True)
    my_ftp.start()


def button4_pause():
    t3 = Pause()
    t3.start()


if __name__ == '__main__':
    app = MyApp()
    section = Section()
    menu = Menu(app, tearoff=0)
    menu.add_command(label="复制", command=section.oncopy)
    menu.add_separator()
    menu.add_command(label="粘贴", command=section.onpaste)
    menu.add_separator()
    menu.add_command(label="剪切", command=section.oncut)

    def popupmenu(event):
        menu.post(event.x_root, event.y_root)
    MyApp.entry.bind("<Button-3>", popupmenu)
    app.mainloop()
