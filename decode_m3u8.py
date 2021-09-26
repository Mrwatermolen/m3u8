from sys import prefix
import requests
from Crypto.Cipher import AES  # pip3 install pycryptodome

from contextlib import closing
import binascii
import os
import time
# from requests import status_codes
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


class ProgressBar(object):

    def __init__(self, title,
                 count=0.0,
                 run_status=None,
                 fin_status=None,
                 total=100.0,
                 unit='', sep='/',
                 chunk_size=1.0):
        super(ProgressBar, self).__init__()
        self.info = "【%s】%s %.2f %s %s %.2f %s"
        self.title = title
        self.total = total
        self.count = count
        self.chunk_size = chunk_size
        self.status = run_status or ""
        self.fin_status = fin_status or " " * len(self.status)
        self.unit = unit
        self.seq = sep

    def __get_info(self):
        # 【名称】状态 进度 单位 分割线 总数 单位
        _info = self.info % (self.title, self.status,
                             self.count/self.chunk_size, self.unit, self.seq, self.total/self.chunk_size, self.unit)
        return _info

    def refresh(self, count=1, status=None):
        self.count += count
        # if status is not None:
        self.status = status or self.status
        end_str = "\r"
        if self.count >= self.total:
            end_str = '\n'
            self.status = status or self.fin_status
        print(self.__get_info(), end=end_str)


class DecodeM3u8File:
    def __init__(self, m3u8_url, save_path, prefix_url, key_url):
        self.m3u8_url = m3u8_url
        self.sava_path = save_path
        self.prefix_url = prefix_url
        self.key_url = key_url
        self.is_encrypted = False

    def analyze_m3u8_url(self):
        self.all_content = requests.get(url=self.m3u8_url, verify=False).text
        self.file_line = self.all_content.split("\n")
        if self.file_line[0] != "#EXTM3U":
            raise BaseException("非M3U8的链接")

        is_in_header = True
        counter = 1
        for index, line in enumerate(self.file_line):
            if is_in_header and (not self.is_encrypted) and "EXT-X-KEY" in line:
                self.is_encrypted = True
                key_url_start = line.find("URI=")
                key_url_end = line.find(",", key_url_start)
                print(line[key_url_start:key_url_end])
                self.creat_cryptor()

            if "#EXTINF" in line:
                real_url = self.prefix_url + self.file_line[index + 1]
                file_name = str(counter).zfill(4)
                ts_name = file_name + ".ts"
                counter += 1

                # 可以多线程优化
                """ ts_get = requests.get(real_url, verify=False)
                        with open(os.path.join(self.sava_path, ts_name), 'wb') as v:
                        v.write(ts_get.content)
                        v.flush()
                    print(ts_name + '下载完成') """

                with closing(requests.get(real_url, stream=True)) as response:
                    chunk_size = 1024  # 单次请求最大值
                    content_size = int(
                        response.headers['content-length'])  # 内容体总大小
                    progress = ProgressBar(file_name, total=content_size,
                                           unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
                    with open(os.path.join(self.sava_path, ts_name), "wb") as file:
                        for data in response.iter_content(chunk_size=chunk_size):
                            if self.is_encrypted:
                                file.write(self.cryptor.decrypt(data))
                            else:
                                file.write(data)
                            progress.refresh(count=len(data))

                with open(os.path.join(self.sava_path, "megreList.txt"), 'a') as m:
                    m.write(f"file '{file_name + '.ts'}'\n")
                time.sleep(0.1)

    def get_decrypted_key(self):
        r = requests.get(url=self.key_url, verify=False)
        if r.status_code == 200:
            # key文件是一个二进制字节文件,读取后类型为bytes,该函数将其转为16字节的16进制字符串
            # self.key = binascii.b2a_hex(r.content) 用python解密不用转为16进制了
            # openssl aes-128-cbc -d -in 1.ts -out 11.ts -nosalt -iv iv -K key
            self.key = r.content
            print(f"Key is :{binascii.b2a_hex(self.key).decode()}\n")

    def creat_cryptor(self, mode="aes-128-cbc", vi=None):
        if vi is None:
            vi = self.key
        if mode == "aes-128-cbc":
            print(f"encrytedFile! mode: {mode}\n")
            self.cryptor = AES.new(self.key, AES.MODE_CBC, self.key)


m3u8_url = "https://i.baobuzz.com/ipfs/QmansQHZzMetzPucghCVXdTkGD75NCrFxyJHZKm6TeP4Up/dan.m3u8"
r = requests.get(url=m3u8_url)
if r.status_code == 200:
    with open(file="C:\\Users\\My computer\\桌面\\dan.m3u8", mode="w") as f:
        f.write(r.text)
# C:\Users\My computer\桌面\dan.m3u8
# https://bafybeifzaozcmt4sxyprpjt27vokwtli5ega2frvyterpct3a3rxqjej7e.ipfs.dweb.link/
# https://cf-ipfs.com/ipfs/QmansQHZzMetzPucghCVXdTkGD75NCrFxyJHZKm6TeP4Up/dan.key
m3u8_url = input("m3u8 url")
save_path = input("save_path")
prefix_url = input("prefix_url")
key_url = input("key_url")
''' m3u8_file = "C:\\Users\\My computer\\桌面\\dan.m3u8"
save_path = "C:\\Users\\My computer\\桌面\\3"
prefix_url = "https://bafybeifzaozcmt4sxyprpjt27vokwtli5ega2frvyterpct3a3rxqjej7e.ipfs.dweb.link/"
key_url = "https://cf-ipfs.com/ipfs/QmansQHZzMetzPucghCVXdTkGD75NCrFxyJHZKm6TeP4Up/dan.key" '''


Downloader = DecodeM3u8File(m3u8_url, save_path, prefix_url, key_url)
Downloader.get_decrypted_key()
Downloader.analyze_m3u8_url()
