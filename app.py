import json
import os
import time

from decode_m3u8 import DecodeM3u8File

DEBUGMODE = False

if DEBUGMODE:
    import tkinter
    from tkinter import filedialog

if __name__ == '__main__':
    with open(file=os.path.join(os.getcwd(), "config.json"), mode="r") as f:
        config = json.load(f)
        print(config)
    decode_m3u8_config = config['decode_m3u8_config']

    vedio_name = decode_m3u8_config.get('vedio_name')
    m3u8_file = decode_m3u8_config.get('m3u8_file')
    save_path = decode_m3u8_config.get('save_path')
    m3u8_url = decode_m3u8_config.get('m3u8_url')
    prefix_url = decode_m3u8_config.get('prefix_url')
    key_url = decode_m3u8_config.get('key_url')
    download_ts_nums = decode_m3u8_config.get('download_ts_nums')

try:
    if not DEBUGMODE:
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        start_time = time.time()
        Downloader = DecodeM3u8File(m3u8_file=m3u8_file, m3u8_url=m3u8_url, save_path=save_path,
                                    prefix_url=prefix_url, key_url=key_url, vedio_name=vedio_name, download_ts_nums=download_ts_nums)
        Downloader.run()
        end_time = time.time()
        print(
            f"[Message] Running time: {int(end_time - start_time)} Seconds")
    else:
        root = tkinter.Tk()
        root.withdraw()
        m3u8_file = filedialog.askopenfilename()
        save_path = filedialog.askdirectory()
        playlist = filedialog.askopenfilename()
        # key_path = filedialog.askopenfilename()
        # with open(key_path,'rb') as f:
        #    key=f.read()
        # Downloader = DecodeM3u8File(m3u8_file=m3u8_file, m3u8_url=m3u8_url, save_path=save_path,
        #                             prefix_url=prefix_url, key_url=key_url, vedio_name=vedio_name, download_ts_nums=1)
        # Downloader.run()
        # download_from_playlist(
        #     playlist=playlist, save_path=save_path, end_line=1)
        # Downloader.megre_mp4(vedio_name=vedio_name)
except BaseException as e:
    print(e)
