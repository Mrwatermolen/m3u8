# -*- coding:utf-

import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from Crypto.Cipher import AES  # pip3 install pycryptodome

from contextlib import closing
import binascii
import os
import time
import json

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

import ProgressBar


class DecodeM3u8File:
    def __init__(self, m3u8_url, save_path, prefix_url, key_url):
        self.m3u8_url = m3u8_url
        self.save_path = save_path
        self.prefix_url = prefix_url
        self.key_url = key_url
        self.is_encrypted = False
        self.play_list = []

    def analyze_m3u8_url(self):
        self.all_content = requests.get(
            url=self.m3u8_url, verify=False).text
        self.file_line = self.all_content.split("\n")
        if self.file_line[0] != "#EXTM3U":
            raise BaseException("非M3U8的链接")
        else:
            with open(os.path.join(self.save_path, self.m3u8_url.rsplit('/', 1)[-1]), "w") as f:
                f.write(self.all_content)

        is_in_header = True
        for index, line in enumerate(self.file_line):
            if is_in_header and (not self.is_encrypted) and "EXT-X-KEY" in line:
                self.is_encrypted = True

                key_url_start = line.find("URI=")
                key_url_end = line.find(",", key_url_start)
                print(line[key_url_start:key_url_end])
                self.__get_decrypted_key()

            if "#EXTINF" in line:
                if "http" in self.file_line[index + 1]:
                    # ts url存在于m3u8文件中，无需拼接
                    self.play_list.append(self.file_line[index + 1])
                else:
                    self.play_list.append(
                        self.prefix_url + self.file_line[index + 1])

        with open(os.path.join(self.save_path, "play_list.txt"), "w") as f:
            for url in self.play_list:
                f.write(url)
                f.write("\n")
        print("m3u8 analyze finished! start to download\n")

        for index, real_url in enumerate(self.play_list):
            file_name = str(index).zfill(4)
            print(f"{index + 1}/{len(self.play_list)}\n")
            self.get_ts(real_url=real_url,
                        file_name=file_name, chunk_size=1024)
            with open(os.path.join(self.save_path, "megreList.txt"), 'a') as m:
                m.write(f"file '{file_name + '.ts'}'\n")
            time.sleep(0.1)
            print("SLEEP\n")

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
            self.cryptor = AES.new(self.key, AES.MODE_CBC, self.key)

    def get_ts(self, real_url, file_name, chunk_size=1024):
        ts_name = file_name + ".ts"
        with closing(requests.get(real_url, stream=True)) as response:
            if response.status_code == 200:
                if 'content-length' in response.headers:
                    content_size = int(
                        response.headers['content-length'])  # 内容体总大小
                else:
                    print(str(response.headers))
                    content_size = 1000000
                progress = ProgressBar(file_name, total=content_size,
                                       unit="KB", chunk_size=chunk_size, run_status="正在下载", fin_status="下载完成")
                with open(os.path.join(self.save_path, ts_name), "wb") as file:
                    for data in response.iter_content(chunk_size=chunk_size):
                        if self.is_encrypted:
                            file.write(self.cryptor.decrypt(data))
                        else:
                            file.write(data)
                        progress.refresh(count=len(data))
            else:
                print(
                    f"response.status_code:{response.status_code}")
                raise BaseException(
                    f"response.status_code:{response.status_code}")


# m3u8_url = "https://i.baobuzz.com/ipfs/QmansQHZzMetzPucghCVXdTkGD75NCrFxyJHZKm6TeP4Up/dan.m3u8"
# C:\Users\My computer\桌面\dan.m3u8
# https://bafybeifzaozcmt4sxyprpjt27vokwtli5ega2frvyterpct3a3rxqjej7e.ipfs.dweb.link/
# https://cf-ipfs.com/ipfs/QmansQHZzMetzPucghCVXdTkGD75NCrFxyJHZKm6TeP4Up/dan.key
if __name__ == '__main__':
    """ with open(file=os.path.join(os.getcwd(), "config.json"), mode="r") as f:
        config = json.load(f)
        print(config)
    vedio_name = config["vedio_name"]
    m3u8_url = config["m3u8_url"]
    save_path = config["save_path"]
    prefix_url = config["prefix_url"]
    key_url = config["key_url"] """
    vedio_name = ""
    m3u8_url = "https://i.baobuzz.com/ipfs/QmansQHZzMetzPucghCVXdTkGD75NCrFxyJHZKm6TeP4Up/dan.m3u8"
    m3u8_file = ""
    save_path = "C:\\Users\\My computer\\桌面\\2"
    prefix_url = "https://bafybeifzaozcmt4sxyprpjt27vokwtli5ega2frvyterpct3a3rxqjej7e.ipfs.dweb.link/"
    key_url = "https://cf-ipfs.com/ipfs/QmansQHZzMetzPucghCVXdTkGD75NCrFxyJHZKm6TeP4Up/dan.key"
    try:
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        Downloader = DecodeM3u8File(m3u8_url, save_path, prefix_url, key_url)
        Downloader.analyze_m3u8_url()
        Downloader.megre_mp4(vedio_name)
    except BaseException as e:
        print(e)
