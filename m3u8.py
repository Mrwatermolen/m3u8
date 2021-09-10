# -*- coding:utf-
import requests
import os
import time
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
DEBUGMODE = False
# Only run on Linux


def download_ts(m3u8_url, save_path):
    # 解析文本信息
    all_content = requests.get(url=m3u8_url, verify=False).text
    file_line = all_content.split("\n")
    if file_line[0] != "#EXTM3U":
        raise BaseException("非M3U8的链接")
    else:
        play_url = m3u8_url.replace(m3u8_url.rsplit('/', 1)[-1], "")
        counter = 1
        for index, line in enumerate(file_line):

            if "#EXTINF" in line:

                pd_url = play_url + file_line[index + 1]
                res = requests.get(pd_url, verify=False)
                ts_name = str(counter).zfill(4) + ".ts"
                counter += 1
                with open(save_path + '/' + ts_name, 'ab') as f:
                    f.write(res.content)
                    f.flush()
                print(ts_name + '下载完成')
                with open(os.path.join(save_path, "megreList.txt"), 'a') as f:
                    f.write(f"file '{ts_name}'\n")


def megre_mp4(save_path, vedio_name, megre_list):

    # vedio_name = "The.Bond.2021.E27.1080p.WEB-DL.AVC.AAC-风尘书断@RS"
    # save_path = input("Save path:")

    vedio_name = os.path.join(save_path, vedio_name)
    command = f"ffmpeg -f concat -i {megre_list} -acodec copy -vcodec copy -absf aac_adtstoasc {vedio_name}.mp4"
    os.system(command)


def make_torrent(hash_path, torrent_save_path=None, m3u8_file=None):
    """
    """
    print("make_torrent\n")
    if torrent_save_path == None or torrent_save_path == "":
        torrent_save_path = hash_path

    if DEBUGMODE:
        print(
            f"m3u8_file:{m3u8_file} is os.path.exists {os.path.exists(m3u8_file)}\n")
        print(
            f"hash_path:{hash_path} is os.path.exists {os.path.exists(hash_path)} is os.path.isfile {os.path.isfile(hash_path)}\n")
        print(
            f"torrent_save_path:{torrent_save_path} is os.path.exists {os.path.exists(torrent_save_path)} is os.path.isfile {os.path.isfile(torrent_save_path)}\n")
    if not os.path.exists(hash_path):
        raise BaseException("Invilad hash path")
    torrent_name = input("torrent_name")

    if os.path.isfile(hash_path):
        if os.path.isfile(torrent_save_path):
            raise BaseException("Invilad save torrent path")
        if not os.path.exists(torrent_save_path):
            os.mkdir(torrent_save_path)
        print(
            f"current save path:{torrent_save_path}, make file {hash_path}\n")
    else:
        # trying to delete m3u8 file in save path to avoid hashing it
        if m3u8_file and os.path.exists(m3u8_file):
            print("try to delete m3u8_file")
            os.remove(m3u8_file)

        print(
            f"current save path:{torrent_save_path}, make all file in this dir and save torrent to there\n")

    command = f"mktorrent -l 22 -p -v -o {os.path.join(torrent_save_path, torrent_name)} {hash_path}"
    os.system(command)


def do_work(save_path, m3u8_url, vedio_name):
    # save_path:存放合成完毕的视频以及种子等, temp存放ts流文件和错误信息和mergeList
    try:
        if not os.path.exists(save_path):
            os.mkdir(save_path)
        temp_dir = os.path.join(save_path, vedio_name)
        if not os.path.exists(temp_dir):
            os.mkdir(temp_dir)

        download_ts(m3u8_url=m3u8_url, save_path=temp_dir)
        megre_mp4(save_path=save_path, vedio_name=vedio_name,
                  megre_list=os.path.join(temp_dir, "megreList.txt"))
        os.system(f"rm -rf {temp_dir}")
    except BaseException as e:
        with open(os.path.join(temp_dir, "errors.log"), 'a') as f:
            f.write(f"Timestamp:{time.time()} errors occur: '{e}'\n")
        print(e)
        return False
    return True


def do_debug():
    kind = int(input("do_work 1, download_ts 2, megre_mp4 3, make_torrent 4\n"))
    save_path = input("save_path:")
    m3u8_file = input("m3u8_file:")
    m3u8_url = input("m3u8_url:")
    vedio_name = input("vedio name:")
    torrent_save_path = input("torrent_save_path:")
    if kind == 1:
        do_work(save_path=save_path, m3u8_url=m3u8_url, vedio_name=vedio_name)
    elif kind == 2:
        download_ts()
    elif kind == 3:
        megre_mp4()
    elif kind == 4:
        make_torrent(hash_path=save_path,
                     torrent_save_path=torrent_save_path, m3u8_file=m3u8_file)
    return


if __name__ == '__main__':
    if DEBUGMODE:
        do_debug()
    else:
        # save_path = "/home/pi/DiskShare/Show/The.Bond.2021/"
        save_path = input("Save path:")
        # m3u8_file = "/home/pi/share/list"
        m3u8_file = input("m3u8 url or urlListPath:")
        isFailed = False  # 是否下载完毕
        vedio_name = ""

        if os.path.exists(m3u8_file) and os.path.isfile(m3u8_file):
            with open(m3u8_file, 'r') as f:
                # 解析list文件内容：vedio_name, m3u8_url
                info = f.read().split("\n")
                for i in info:
                    if i == "":
                        continue
                    vedio_name = i.split(",")[0]
                    m3u8_url = i.split(",")[-1]
                    if do_work(save_path=save_path, m3u8_url=m3u8_url, vedio_name=vedio_name):
                        print(vedio_name + '下载完成')
                    else:
                        print(vedio_name + '下载失败')
                        isFailed = True
        else:
            vedio_name = input("Vedio name:")
            if do_work(save_path=save_path, m3u8_url=m3u8_file, vedio_name=vedio_name):
                print(vedio_name + '下载完成')
            else:
                print(vedio_name + '下载失败')
                isFailed = True

        if (not isFailed) and (input("input -1 to exit make torrent") != "-1"):
            if input("input 1 to make torrent for a file but dir") == "1":
                torrent_save_path = input("torrent_save_path:")
                make_torrent(hash_path=os.path.join(
                    save_path, vedio_name + ".mp4"), torrent_save_path=torrent_save_path)
            make_torrent(save_path, m3u8_file=os.path.join(
                save_path, m3u8_file))

    '''     if not os.path.exists(save_path):
            os.mkdir(save_path)

        if os.path.exists(m3u8_file) and os.path.isfile(m3u8_file):
            with open(m3u8_file, 'r') as f:
                # 解析list文件内容：vedio_name, m3u8_url
                info = f.read().split("\n")
                for i in info:
                    if i == "":
                        continue
                    vedio_name = i.split(",")[0]
                    m3u8_url = i.split(",")[-1]

                    temp_dir = os.path.join(save_path, vedio_name)

                    if DEBUGMODE:
                        print(f"i:{i}  temp_dir{temp_dir}\n")
                        input("input anything to continue")
                    if not os.path.exists(temp_dir):
                        os.mkdir(temp_dir)

                    if download_ts(m3u8_url=m3u8_url, save_path=temp_dir):
                        megre_mp4(save_path=save_path, vedio_name=vedio_name,
                                megre_list=os.path.join(temp_dir, "megreList.txt"))
                        os.system(f"rm -rf {temp_dir}")

        else:
            vedio_name = input("Vedio name:")
            temp_dir = os.path.join(save_path, vedio_name)

            if not os.path.exists(temp_dir):
                os.mkdir(temp_dir)

            if download_ts(m3u8_url=m3u8_file, save_path=temp_dir):
                megre_mp4(save_path, vedio_name, megre_list=os.path.join(
                    temp_dir, "megreList.txt"))
                os.system(f"rm -rf {temp_dir}") '''
