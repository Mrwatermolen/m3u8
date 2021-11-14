# -*- coding:utf-

from requests.api import head
from multipleThreadDownloader import MultipleThreadDownloader
from contextlib import closing
import binascii
import os
import time

import re
import threading

import requests
from Crypto.Cipher import AES  # pip3 install pycryptodome
from tqdm import tqdm

def download_from_playlist(playlist, save_path, start_line=None, end_line=None, key=None, cryptor=None, num=1):
    with open(playlist, 'r') as f:
        url_list = f.readlines()
        start_line = start_line or 0
        end_line = end_line or len(url_list)
        download_urls = []
        thread_list = []
        if not key is None:
            cryptor = AES.new(key, AES.MODE_CBC, key)

        # for index, url in enumerate(url_list):
        #     if start_line <= index and index < end_line:
        #         ts_name = str(index).zfill(4) + '.ts'
        #         download_urls.append((ts_name, url.replace('\n', '')))
        #         downloader = MultipleThreadDownloader(
        #             url=url, save_path=save_path, file_name=ts_name, cryptor=cryptor)
        #         thread = threading.Thread(
        #             target=downloader.run)
        #         thread.start()
        #         thread_list.append(thread)
        counter = 0
        for url in url_list[start_line:end_line:num]:
            for index in range(0, num):
                if (counter * num + start_line + index) >= end_line:
                    break
                ts_name = str(counter * num + start_line +
                              index).zfill(4) + '.ts'
                download_urls.append((ts_name, url.replace('\n', '')))
                downloader = MultipleThreadDownloader(
                    url=url, save_path=save_path, file_name=ts_name, cryptor=cryptor, thread_num=4)
                thread = threading.Thread(
                    target=downloader.run)

                thread.start()
                thread_list.append(thread)
            for i in range(0, num):
                if (i + counter * num) >= len(thread_list):
                    break
                thread_list[i + counter * num].join()
            counter += 1


class DecodeM3u8File:
    """ 
    params:
        download_ts_nums: number of ts downloaded at the same time
    """

    def __init__(self, m3u8_file, m3u8_url, save_path, prefix_url, key_url, vedio_name, download_ts_nums=1):
        super(DecodeM3u8File, self).__init__()
        self.m3u8_file = m3u8_file
        self.m3u8_url = m3u8_url
        self.save_path = save_path
        self.prefix_url = prefix_url or m3u8_url.replace(
            m3u8_url.rsplit('/', 1)[-1], "")
        self.key_url = key_url
        self.vedio_name = vedio_name
        self.download_ts_nums = download_ts_nums

        self.play_list = []
        self.ts_size = []
        self.total_size = 0
        self.ts_finish = []
        self.cryptor = None
        self.accept_range = 'bytes'
        self.headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

    def analyze_m3u8(self):

        # get m3u8 info
        if os.path.exists(self.m3u8_file):
            with open(self.m3u8_file, 'r') as f:
                self.all_content = f.read()
        elif self.m3u8_url:
            self.all_content = requests.get(
                url=self.m3u8_url, verify=False).text
        self.file_line = self.all_content.split("\n")
        if self.file_line[0] != "#EXTM3U":
            raise BaseException("Non m3u8")

        # analyze
        is_in_header = True
        is_encrypted = False
        for index, line in enumerate(self.file_line):
            # whether this vedio is decrypted
            if is_in_header and (not is_encrypted) and "EXT-X-KEY" in line:
                is_encrypted = True
                # key_url_start = line.find("URI=")
                # key_url_end = line.find(",", key_url_start)
                # print(line[key_url_start:key_url_end])
                self.get_decrypted_key()
            # get real url
            if "#EXTINF" in line:
                is_in_header = False
                self.ts_finish.append(True)
                if "http" in self.file_line[index + 1]:
                    # the url of ts exists in the m3u8 file
                    self.play_list.append(self.file_line[index + 1])
                else:
                    self.play_list.append(
                        self.prefix_url + self.file_line[index + 1])

        # analyze vedio and record
        """ a = time.time()
        with open(os.path.join(self.save_path, "play_list.txt"), "w") as f:
            for index, url in enumerate(self.play_list):
                c = time.time()
                max_retry = 10
                is_finished = False

                while max_retry:
                    try:
                        # first try to get header
                        header = {
                            'User-Agent': 'QYPlayer/Android/4.4.5;NetType/3G;QTP/1.1.4.3'}
                        r = requests.head(url, proxies={}, headers=header)
                        while r.status_code == 302:
                            r.close()
                            r = requests.head(
                                url, proxies={}, allow_redirects=True)
                            # if not 302, history will don't exist!
                            url = r.history[-1].headers.get('location')
                        if r.status_code >= 400:
                            raise ConnectionError(
                                f"Connection failed! Response {r.status_code}")
                        # get ts info
                        file_size = r.headers.get('Content-Length')
                        self.accept_range = r.headers.get(
                            'Accept-Ranges') or self.accept_range
                        if file_size is None:
                            file_size = 0
                        self.ts_size.append(int(file_size))
                        self.total_size += int(file_size)
                        self.play_list[index] = url
                        is_finished = True
                        f.write(url)
                        f.write("\n")
                        d = time.time()
                        # download progress should be there
                        print(
                            f"total number: {len(self.play_list)}, cur {index} ts size: {(int(file_size)/1024.0):05.2f} KB. spent {(d - c):05.2f} seconds")
                        break
                    except Exception as e:
                        max_retry -= 1
                        print(
                            f"cur {index} ts error {e}. remain retry times {max_retry}")

                if not is_finished:
                    self.ts_size.append(0)
                    with open(os.path.join(self.save_path, 'error.log'), 'w') as f:
                        pass

        b = time.time()
        print(
            f"m3u8 analyzes finished! spent time: {(b - a):05.2f} start to download {(self.total_size/1024.0):07.2f}.") """

    def get_ts(self, url, file_name, ts_size, start=None, end=None):
        ts_name = file_name + ".ts"
        downloader = MultipleThreadDownloader(
            url=url, save_path=self.save_path, file_name=ts_name, file_size=ts_size, cryptor=self.cryptor, thread_num=8)
        if start is None and end is None:
            downloader.run()
        else:
            downloader.single_thread_download(start=start, end=end)

    def megre_mp4(self, vedio_name):
        megre_list = os.path.join(self.save_path, "megreList.txt")
        vedio = os.path.join(self.save_path, vedio_name)
        print(self.save_path)
        command = f"ffmpeg -f concat -i {megre_list} -acodec copy -vcodec copy -absf aac_adtstoasc {vedio}.mp4"
        print(command)
        os.system(command)

    def get_decrypted_key(self):
        r = requests.get(url=self.key_url, verify=False)
        if r.status_code == 200:
            # key文件是一个二进制字节文件,读取后类型为bytes,该函数将其转为16字节的16进制字符串
            # self.key = binascii.b2a_hex(r.content) 用python解密不用转为16进制了
            # openssl aes-128-cbc -d -in 1.ts -out 11.ts -nosalt -iv iv -K key
            self.key = r.content
            print(f"Key is :{binascii.b2a_hex(self.key).decode()}\n")
            with open(os.path.join(self.save_path, "key.key"), "wb") as f:
                f.write(r.content)
            self.cryptor = self.creat_cryptor()

    def creat_cryptor(self, mode="aes-128-cbc", vi=None):
        if vi is None:
            vi = self.key
        if mode == "aes-128-cbc":
            print(f"encrytedFile! mode: {mode}\n")
            return AES.new(self.key, AES.MODE_CBC, self.key)

    def run(self):
        self.analyze_m3u8()

        """ self.bar = tqdm(total=self.total_size/1024,
                        desc=f'download file：{self.vedio_name}') """

        # try to download
        error_log = open(os.path.join(self.save_path, 'error.log'), 'w')
        error_log, os.close
        thread_list = []
        counter = 0
        for url in self.play_list[0:len(self.play_list):self.download_ts_nums]:
            for index in range(0, self.download_ts_nums):
                if (counter * self.download_ts_nums + index) >= len(self.play_list):
                    break
                file_name = str(counter * self.download_ts_nums +
                                index).zfill(4)
                thread = threading.Thread(
                    target=self.get_ts, args=(url, file_name, 0))
                thread.start()
                thread_list.append(thread)
                with open(os.path.join(self.save_path, "megreList.txt"), 'a') as m:
                    m.write(f"file '{file_name + '.ts'}'\n")
            for i in range(0, self.download_ts_nums):
                if (i + counter * self.download_ts_nums) >= len(thread_list):
                    break
                thread_list[i + counter * self.download_ts_nums].join()
            counter += 1

        # retry
        ''' i = 0
        for index, real_url in enumerate(self.play_list):
            if not self.ts_finish[index]:
                file_name = str(index).zfill(4) '''

        self.megre_mp4(self.vedio_name)  # save path cann't include ' '
