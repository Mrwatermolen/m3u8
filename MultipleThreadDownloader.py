# -*- coding: utf-8 -*-

import threading
import os
import time
from tkinter.constants import NO

import requests
from tqdm import tqdm
from Crypto.Cipher import AES

lock = threading.Lock()


class MultipleThreadDownloader(object):
    def __init__(self, url, save_path, file_name, thread_num=1, file_size=0, accept_ranges='bytes', cryptor=None):
        super(MultipleThreadDownloader, self).__init__()
        self.url = url
        self.save_path = save_path
        self.file_name = file_name
        self.thread_num = thread_num
        self.file_size = file_size
        self.accept_ranges = accept_ranges
        self.cryptor = cryptor

        self.is_complete = True

    def get_range(self):

        # Whether it can be to split
        if self.file_size == 0 or self.accept_ranges is None:
            # res = requests.head(self.url,allow_redirects=True) # fuck iqiyi: <Response [302]>. set {allow_redirects=True} will lost arg: Range
            # 'set {allow_redirects=True} will lost arg: Range' is wrong. sometime
            res = requests.head(self.url)
            while res.status_code == 302:
                self.url = res.headers.get('location')
                # print(f"{res.headers.get('Content-Length')}  {res.headers.get('Accept-Ranges')}")
                # print(f"{res.headers.get('location')}")
                res.close()
                res = requests.head(self.url)
            # print(res.headers)

            file_size = int(res.headers.get('Content-Length'))
            self.accept_ranges = res.headers.get(
                'Accept-Ranges') or self.accept_ranges
            if file_size is None or self.accept_ranges is None:
                raise ValueError("This file does not support MTD!")
            self.file_size = file_size
            # self.url = res.url

        # Generate range for each block
        offset = int(self.file_size / self.thread_num)
        parts = [(start, min(start+offset, self.file_size))
                 for start in range(0, self.file_size, offset)]

        return parts

    def single_thread_download(self, start=None, end=None, chunk_size=1024, max_retry=10):

        # set header
        if start is None and end is None:
            # Range accept different arg such as bytes or Bytes. TT
            headers = {
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                'Range': f'{self.accept_ranges}={start}-{end}',
                'Accept-Encoding': '*'
            }
        else:
            headers = {
                'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
                'Accept-Encoding': '*'
            }
        download_succeed = False
        data = []
        msg = ''
        while max_retry:
            try:
                requests.adapters.DEFAULT_RETRIES = 10  # set times of recoonection
                # s = requests.session()
                res = requests.get(self.url, stream=True,
                                   headers=headers, allow_redirects=True, proxies={})
                for chunk in res.iter_content(chunk_size=chunk_size):
                    data.append(chunk)
                    if not self.bar is None:
                        self.bar.update(len(chunk)/chunk_size)
                download_succeed = True
                break
            except Exception as e:
                download_succeed = False
                msg = f"file:{self.file_name} block: {start}-{end} occurs errors! Error: {e}\n remain times:{max_retry - 1}"
                print(msg)
                max_retry -= 1

        if download_succeed:
            with lock:  # Process lock protects file from being wrote in same time, but actually it can be commented out because local variable is safe
                # the file pointer can move anywhere in rb mode but
                if not start is None:
                    with open(os.path.join(self.save_path, self.file_name), 'rb+') as file:
                        file.seek(start)
                        for temp in data:
                            file.write(temp)
                else:
                    with open(os.path.join(self.save_path, self.file_name), 'wb') as file:
                        for temp in data:
                            file.write(temp)
        else:
            with lock:
                error_log = open(os.path.join(
                    self.save_path, 'error.log'), 'a')
                error_log.write(msg)
                error_log.close()
                self.is_complete = False
            # raise BaseException(msg)

    def run(self):

        # Ensure that the file exists to avoid failing to write in rb mode
        prepare_file = open(os.path.join(self.save_path, self.file_name), 'wb')
        prepare_file.truncate(self.file_size)  # d
        prepare_file.close()
        thread_list = []
        try:
            parts = self.get_range()
            self.bar = tqdm(total=(self.file_size/1024),
                            desc=f'download file：{self.file_name}')
        except Exception as e:
            print(f"get_range() occurs error! Error: {e}")
            parts = [(None, None)]
            self.bar = None

        # print(type(self.cryptor))

        # assign block
        for ran in parts:
            start, end = ran
            thread = threading.Thread(
                target=self.single_thread_download, args=(start, end))
            thread.start()
            thread_list.append(thread)

        # wait to pre thread finish
        for i in thread_list:
            i.join()

        # Data must be padded to 16 byte boundary in CBC mode
        if self.is_complete and not self.cryptor is None:
            with open(os.path.join(self.save_path, self.file_name), 'rb') as f:
                encryte_data = f.read()
            with open(os.path.join(self.save_path, self.file_name), 'wb') as f:
                f.write(self.cryptor.decrypt(encryte_data))


""" if __name__ == '__main__':
    url = 'https://issuecdn.baidupcs.com/issue/netdisk/yunguanjia/BaiduNetdisk_7.2.8.9.exe'
    save_path = 'C:\\Users\\My computer\\桌面\\3'
    file_name = 'BaiduNetdisk_7.2.8.9.exe'
    file_size = int(requests.head(url).headers.get('Content-Length'))
    test = MultipleThreadDownloader(
        url=url, save_path=save_path, file_name=file_name, file_size=file_size)
    test.run() """
