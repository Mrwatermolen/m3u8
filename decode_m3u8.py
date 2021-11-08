# -*- coding:utf-

from contextlib import closing
import binascii
import os
import time
import json

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from Crypto.Cipher import AES  # pip3 install pycryptodome
from tqdm import tqdm

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

from MultipleThreadDownloader import MultipleThreadDownloader

class DecodeM3u8File:
    def __init__(self, m3u8_file, m3u8_url, save_path, prefix_url, key_url, vedio_name):
        super(DecodeM3u8File, self).__init__()
        self.m3u8_file = m3u8_file
        self.m3u8_url = m3u8_url
        self.save_path = save_path
        self.prefix_url = prefix_url
        self.key_url = key_url
        self.vedio_name = vedio_name

        self.is_encrypted = False
        self.play_list = []
        self.ts_size = []
        self.total_size = 0
        self.ts_finish = []
        self.headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}

    def analyze_m3u8_url(self):

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
        for index, line in enumerate(self.file_line):
            # whether this vedio is decrypted
            if is_in_header and (not self.is_encrypted) and "EXT-X-KEY" in line:
                self.is_encrypted = True
                key_url_start = line.find("URI=")
                key_url_end = line.find(",", key_url_start)
                print(line[key_url_start:key_url_end])
                self.__get_decrypted_key()
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
        a = time.time()
        with open(os.path.join(self.save_path, "play_list.txt"), "w") as f:
            for index, url in enumerate(self.play_list):
                c = time.time()
                f.write(url)
                f.write("\n")
                r = requests.head(url, headers=self.headers)
                file_size = r.headers.get('Content-Length')
                if file_size is None:
                    file_size = 0
                self.ts_size.append(int(file_size))
                self.total_size += int(file_size)
                d = time.time()
                print(f"total number: {len(self.play_list)}, cur {index + 1} ts size: {file_size}. spent {d - c}")
        b = time.time()
        print(f"m3u8 analyzes finished! spent time: {b - a} start to download {self.total_size}.")

        self.bar = tqdm(total=self.total_size,desc=f'download file：{self.vedio_name}')

        # try to download
        for index, real_url in enumerate(self.play_list):
            file_name = str(index).zfill(4)
            try:
                self.get_ts(real_url=real_url,
                            file_name=file_name, ts_size=self.ts_size[index])
                with open(os.path.join(self.save_path, "megreList.txt"), 'a') as m:
                    m.write(f"file '{file_name + '.ts'}'\n")
                self.bar.update(self.ts_size[index])
            except Exception as e:
                self.ts_finish[index] = False
                err = f"ts: {file_name} download fail! Error: {e}"
                print(err)

    def get_ts(self, real_url, file_name, ts_size):
        ts_name = file_name + ".ts"
        downloader = MultipleThreadDownloader(
            url=real_url, save_path=self.save_path, file_name=ts_name, file_size=ts_size)
        downloader.run()

    def megre_mp4(self, vedio_name):
        megre_list = os.path.join(self.save_path, "megreList.txt")
        vedio = os.path.join(self.save_path, vedio_name)
        print(self.save_path)
        command = f"ffmpeg -f concat -i {megre_list} -acodec copy -vcodec copy -absf aac_adtstoasc {vedio}.mp4"
        print(command)
        os.system(command)

    def __get_decrypted_key(self):
        r = requests.get(url=self.key_url, verify=False)
        if r.status_code == 200:
            # key文件是一个二进制字节文件,读取后类型为bytes,该函数将其转为16字节的16进制字符串
            # self.key = binascii.b2a_hex(r.content) 用python解密不用转为16进制了
            # openssl aes-128-cbc -d -in 1.ts -out 11.ts -nosalt -iv iv -K key
            self.key = r.content
            print(f"Key is :{binascii.b2a_hex(self.key).decode()}\n")
            with open(os.path.join(self.save_path, "key.key"), "wb") as f:
                f.write(r.content)
            self.__creat_cryptor()

    def __creat_cryptor(self, mode="aes-128-cbc", vi=None):
        if vi is None:
            vi = self.key
        if mode == "aes-128-cbc":
            print(f"encrytedFile! mode: {mode}\n")
            return AES.new(self.key, AES.MODE_CBC, self.key)


if __name__ == '__main__':
    """ with open(file=os.path.join(os.getcwd(), "config.json"), mode="r") as f:
        config = json.load(f)
        print(config)
    vedio_name = config["vedio_name"]
    m3u8_url = config["m3u8_url"]
    save_path = config["save_path"]
    prefix_url = config["prefix_url"]
    key_url = config["key_url"] """
    vedio_name = "ddd"
    m3u8_url = "https://i.baobuzz.com/ipfs/QmansQHZzMetzPucghCVXdTkGD75NCrFxyJHZKm6TeP4Up/dan.m3u8"
    m3u8_file = ""
    save_path = "C:\\Users\\My computer\\桌面\\2"
    prefix_url = "https://bafybeifzaozcmt4sxyprpjt27vokwtli5ega2frvyterpct3a3rxqjej7e.ipfs.dweb.link/"
    key_url = "https://cf-ipfs.com/ipfs/QmansQHZzMetzPucghCVXdTkGD75NCrFxyJHZKm6TeP4Up/dan.key"
    try:
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        start_time = time.time()
        Downloader = DecodeM3u8File(m3u8_file=m3u8_file, m3u8_url=m3u8_url, save_path=save_path,
                                    prefix_url=prefix_url, key_url=key_url, vedio_name=vedio_name)
        Downloader.analyze_m3u8_url()
        # Downloader.megre_mp4(vedio_name)
        end_time = time.time()
        print(f"[Message] Running time: {int(end_time - start_time)} Seconds")
    except BaseException as e:
        print(e)
