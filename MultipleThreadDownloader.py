# -*- coding: utf-8 -*-

import threading
import os
import time
from contextlib import closing
from requests.models import to_key_val_list

import requests
from tqdm import tqdm

lock = threading.Lock()


class MultipleThreadDownloader(object):
    def __init__(self, url, save_path, file_name, thread_num=12, file_size=0, cryptor=None):
        super(MultipleThreadDownloader, self).__init__()
        self.url = url
        self.save_path = save_path
        self.file_name = file_name
        self.thread_num = thread_num
        self.file_size = file_size
        self.cryptor = cryptor

        self.bar = tqdm(total=file_size, desc=f'download file：{file_name}')

    def get_range(self):

        # Whether it can be to split
        if self.file_size == 0:
            file_size = int(requests.head(
                self.url).headers.get('Content-Length'))
            if file_size is None:
                raise ValueError("This file does not support MTD!")
            self.file_size = file_size

        # Generate range for each block
        offset = int(self.file_size / self.thread_num)
        parts = [(start, min(start+offset, self.file_size))
                 for start in range(0, self.file_size, offset)]

        return parts

    def single_thread_download(self, start=None, end=None, chunk_size=1024):

        # set header
        headers = {
            'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
            'Range': f'Bytes={start}-{end}',
            'Accept-Encoding': '*'
        }
        download_succeed = False
        data = []
        msg = ''

        try:
            requests.adapters.DEFAULT_RETRIES = 10  # set times of recoonection
            res = requests.get(self.url, stream=True, headers=headers)
            for chunk in res.iter_content(chunk_size=chunk_size):
                if self.cryptor is None:
                    data.append(chunk)
                else:
                    data.append(self.cryptor(chunk))
                self.bar.update(chunk_size)
            download_succeed = True
        except Exception as e:
            download_succeed = False
            msg = f"block: {start}-{end} occurs errors! Error: {e}"
            print(msg)
            

        if download_succeed:
            with lock:  # Process lock protects file from being wrote in same time, but actually it can be commented out because local variable is safe
                # the file pointer can move anywhere in rb mode but
                with open(os.path.join(self.save_path, self.file_name), 'rb+') as file:
                    file.seek(start)
                    for temp in data:
                        file.write(temp)
        else:
            raise BaseException(msg)

    def run(self):

        # Ensure that the file exists to avoid failing to write in rb mode
        prepare_file = open(os.path.join(self.save_path, self.file_name), 'wb')
        prepare_file.truncate(self.file_size)  # d
        prepare_file.close()
        thread_list = []

        # assign block
        for ran in self.get_range():
            start, end = ran
            thread = threading.Thread(
                target=self.single_thread_download, args=(start, end))
            thread.start()
            thread_list.append(thread)

        # wait to pre thread finish
        for i in thread_list:
            i.join()


""" if __name__ == '__main__':
    url = 'https://issuecdn.baidupcs.com/issue/netdisk/yunguanjia/BaiduNetdisk_7.2.8.9.exe'
    save_path = 'C:\\Users\\My computer\\桌面\\3'
    file_name = 'BaiduNetdisk_7.2.8.9.exe'
    file_size = int(requests.head(url).headers.get('Content-Length'))
    test = MultipleThreadDownloader(
        url=url, save_path=save_path, file_name=file_name, file_size=file_size)
    test.run() """
