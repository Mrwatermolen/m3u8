# -*- coding:utf-
import os
fast_table = {"work_name": ["The.Bond.2021.E", "Liu.Yong.Zhui.An.2021.E"],
              "vedio_save_path": ["/home/pi/DiskShare/Show/The.Bond.2021/The.Bond.2021/", "/home/pi/DiskShare/Show/Liu.Yong.Zhui.An.2021/Liu.Yong.Zhui.An.2021/"],
              "resolution": ["720p", "1080p", "2160p"],
              "source": ["WEB-DL", "BDrip", "BluRay"],
              "vedio_encode": ["H264", "AVC", "H265", "HEVC"],
              "audio_encode": ["AAC", "DDP"],
              "maker": ["风尘书断@RS"]}
index = [0, 0, 0, 0, 0, 0, 0]
info = ""

print(str(fast_table))

x = 0
for i in fast_table:
    index[x] = int(input(f"{fast_table[i]} index"))
    print(fast_table[i][index[x]] + "\n")
    x += 1
#PLAYER._DownloadMonitor.context.dataset.currentVideoUrl
dir = fast_table["vedio_save_path"][index[1]]
file_name = fast_table["work_name"][index[0]]
info = fast_table["resolution"][index[2]] + "." + fast_table["source"][index[3]] + "." + fast_table["vedio_encode"][index[4]
                                                                                                                    ] + "." + fast_table["audio_encode"][index[5]] + '-' + fast_table["maker"][index[6]]
print(info)
isAuto = False
n = 2
if not os.path.exists(dir):
    os.mkdir(dir)
with open(os.path.join(dir, "list"), 'w', encoding="utf-8") as f:
    isAuto = True if (
        input("1 == auto from index to 99 or other") == '1') else False
    if isAuto:
        index = int(input("index = ?"))
    while (True):
        if not isAuto:
            index = int(input("Index or -1 == quit\n"))
            if index == -1:
                break
        url = input("m3u8 or -1 == quit\n")
        if url == '-1':
            break
        line = file_name + str(index).zfill(n) + '.' + info + ',' + url + '\n'
        index += 1
        print(line)
        f.write(line)
