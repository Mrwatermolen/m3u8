from logging import fatal
from tqdm import tqdm
from re import T
import time
import tkinter
import os
from tkinter import filedialog
from multipleThreadDownloader import MultipleThreadDownloader
import requests
from requests.api import head

# 1
''' def download_from_playlist(playlist, save_path, start_line=None, end_line=None, cryptor=None):

    with open(playlist, 'r') as f:
        url_list = f.readlines()
        start_line = start_line or 0
        end_line = end_line or len(url_list)
        
        for index, url in enumerate(url_list):
            url = url.replace('\n', '')
            ts_name = str(index).zfill(4) + '.ts'
            if start_line <= index and index < end_line:
                downloader = MultipleThreadDownloader(
                    url=url, save_path=save_path, file_name=ts_name, cryptor=cryptor)
                downloader.run()


root = tkinter.Tk()
root.withdraw()
list = filedialog.askopenfilename()
save = filedialog.askdirectory()
print(list)
download_from_playlist(list, save, 60) '''

# r = requests.head(url='http://221.204.187.46/videos/v0/20211105/70/d8/8f586ffcc7f522ab305a797a0c80bf4a.265ts?key=041dce789e06b2ec0b29fd9e309363483&dis_k=2088f164064c86ec8f5ebf355e4281783&dis_t=1636467069&dis_dz=CNC-Shan3Xi_XiAn&dis_st=139&src=iqiyi.com&dis_hit=0&dis_tag=01210000&uuid=71c8ae06-618a817d-185&br=100&contentlength=6685468&qd_tm=1636464687129&qd_uid=2210438980839424&qd_k=5233213b58aa7e69846ab931a93ec3c5&end=6685468&qd_tvid=4779805475332900&start=0&qd_p=71c8ae06&qyid=4b9036fe9e16710ba22d27800e5b5256&bid=800&qd_index=vod&qd_src=03020031010000000000&sd=0&qd_vip=1&qd_vipres=2&z=taiyuan7_cnc')
# r = requests.head('http://data.video.iqiyi.com/videos/v0/20211105/70/d8/8f586ffcc7f522ab305a797a0c80bf4a.265ts?start=0&end=6685468&contentlength=6685468&sd=0&qdv=2&qd_uid=2210438980839424&qd_vip=1&qd_src=03020031010000000000&qd_tm=1636464687129&qd_p=71c8ae06&qd_k=5233213b58aa7e69846ab931a93ec3c5&qd_index=vod&qd_tvid=4779805475332900&qd_sc=65579fc4ebe234c12a510402183c7d6b&bid=800&qyid=4b9036fe9e16710ba22d27800e5b5256&qd_vipres=2&br=100',allow_redirects=True)
# r = requests.head('https://bafybeifzaozcmt4sxyprpjt27vokwtli5ega2frvyterpct3a3rxqjej7e.ipfs.dweb.link/dan0.png')
# r = requests.head('http://data.video.iqiyi.com/videos/v0/20211105/70/d8/8f586ffcc7f522ab305a797a0c80bf4a.265ts?start=0&end=6685468&contentlength=6685468&sd=0&qdv=2&qd_uid=2210438980839424&qd_vip=1&qd_src=03020031010000000000&qd_tm=1636464687129&qd_p=71c8ae06&qd_k=5233213b58aa7e69846ab931a93ec3c5&qd_index=vod&qd_tvid=4779805475332900&qd_sc=65579fc4ebe234c12a510402183c7d6b&bid=800&qyid=4b9036fe9e16710ba22d27800e5b5256&qd_vipres=2&br=100')
# r = requests.head('http://data.video.iqiyi.com/videos/v0/20211105/9c/9d/be10e87f1284ab4613485503da359981.265ts?start=0&end=1998628&contentlength=1998628&sd=0&qdv=2&qd_uid=2210438980839424&qd_vip=1&qd_src=03020031010000000000&qd_tm=1636469978389&qd_p=71c8ae06&qd_k=8912897b7d59eb66ef71beea09065dfd&qd_index=vod&qd_tvid=2694174271308500&qd_sc=67ec93c2006d7c09a92f6ec3960c7219&bid=800&qyid=4b9036fe9e16710ba22d27800e5b5256&qd_vipres=2&br=100')
# print(r)
# while r.status_code == 302:
#     print(r)
#     print(f"{r.headers.get('Content-Length')}  {r.headers.get('Accept-Ranges')}")
#     print(f"{r.headers.get('location')}")
#     r.close()
#     r = requests.head(r.headers.get('location'))
# print(r)
# print(f"{r.headers.get('Content-Length')}  {r.headers.get('Accept-Ranges')}")
# print(f"{r.headers.get('location')}")

# 2
# import json

# ts_iqiyi_direct = 'http://data.video.iqiyi.com/videos/v0/20211107/b3/fa/36b33221f96c7887b709ea8013631746.265ts?start=6146472&end=10883884&contentlength=4737412&sd=9000&qdv=2&qd_uid=2210438980839424&qd_vip=1&qd_src=03020031010000000000&qd_tm=1636532854610&qd_p=71c8ae08&qd_k=1fc5c4a4466bf30372cb4732a7c7f3c0&qd_index=vod&qd_tvid=7334703700259500&qd_sc=42e2b88424e77e96c7ec9bc986bc61a1&bid=800&qyid=4b9036fe9e16710ba22d27800e5b5256&qd_vipres=2&br=100'
# ts_model_direct = 'https://bafybeifzaozcmt4sxyprpjt27vokwtli5ega2frvyterpct3a3rxqjej7e.ipfs.dweb.link/dan0.png'
# ts_iqiyi_final = 'http://exchang.qnssl.com/baiducdncnc.inter.iqiyi.com/videos/v0/20211105/70/d8/8f586ffcc7f522ab305a797a0c80bf4a.265ts?key=0f867ba4ae7c3e29d708fab9e3b8adf1d&dis_k=391dca59019e3ddf91fc102507295648&dis_t=1636507268&dis_dz=CNC-Shan3Xi_XiAn&dis_st=139&src=iqiyi.com&dis_hit=0&dis_tag=01210000&uuid=71c8ae08-618b1e84-189&br=100&contentlength=6685468&qd_tm=1636464687129&qd_uid=2210438980839424&qd_k=5233213b58aa7e69846ab931a93ec3c5&end=6685468&qd_tvid=4779805475332900&start=0&qd_p=71c8ae06&qyid=4b9036fe9e16710ba22d27800e5b5256&bid=800&qd_index=vod&qd_src=03020031010000000000&sd=0&qd_vip=1&qd_vipres=2&z=baiducdn_cnc'

# res_iqiyi_fasle_redirect = requests.head(ts_iqiyi_direct,allow_redirects=False,proxies={})
# with open(os.path.join('C:/Users/My computer/桌面','res_iqiyi_fasle_redirect.json'),'w') as f:
#     json.dump(dict(res_iqiyi_fasle_redirect.headers), f)
# while res_iqiyi_fasle_redirect.status_code == 302:
#     # res_iqiyi_fasle_redirect.close()
#     res_iqiyi_fasle_redirect = requests.head(res_iqiyi_fasle_redirect.headers.get('location'),proxies={})
#     print(f"{res_iqiyi_fasle_redirect.headers.get('Content-Length')}  {res_iqiyi_fasle_redirect.headers.get('Accept-Ranges')}") # 注意RFC中注明了Accept-Ranges这一部分并不是必须的
#     # print(f"{r.headers.get('location')}")
#     with open(os.path.join('C:/Users/My computer/桌面','res_iqiyi_fasle_redirect.json'),'a') as f:
#         json.dump(dict(res_iqiyi_fasle_redirect.headers), f)

# res_iqiyi_true_redirect = res_iqiyi_fasle_redirect = requests.head(ts_iqiyi_direct,allow_redirects=True,proxies={})
# print(res_iqiyi_true_redirect.status_code)
# with open(os.path.join('C:/Users/My computer/桌面','res_iqiyi_true_redirect.json'),'w') as f:
#     json.dump(dict(res_iqiyi_fasle_redirect.headers), f)
#     # json.dump(dict(res_iqiyi_fasle_redirect.history), f)
# res_iqiyi_final_h = requests.head(url=ts_iqiyi_final,proxies={})
# headers = {
#             'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
#             'Range': 'bytes=1-1025',
#             'Accept-Encoding': '*'
#         }
# res_iqiyi_final = requests.get(url=ts_iqiyi_final,headers=headers,proxies={})
# res_model_fasle_redirect = requests.head(ts_model_direct,allow_redirects=False,proxies={},stream=True)
# res_model_true_redirect = requests.head(ts_model_direct,allow_redirects=True,proxies={})
# res_model = requests.get(url=ts_model_direct,headers=headers,proxies={})
# with open(os.path.join('C:/Users/My computer/桌面','res_model.json'),'w') as f:
#     json.dump(dict(res_model_fasle_redirect), f)

# 3 allow_redirects default False
# ts_iqiyi_direct = 'http://data.video.iqiyi.com/videos/v0/20211107/b3/fa/36b33221f96c7887b709ea8013631746.265ts?start=0&end=6146472&contentlength=6146472&sd=0&qdv=2&qd_uid=2210438980839424&qd_vip=1&qd_src=03020031010000000000&qd_tm=1636532854610&qd_p=71c8ae08&qd_k=1fc5c4a4466bf30372cb4732a7c7f3c0&qd_index=vod&qd_tvid=7334703700259500&qd_sc=42e2b88424e77e96c7ec9bc986bc61a1&bid=800&qyid=4b9036fe9e16710ba22d27800e5b5256&qd_vipres=2&br=100'
# ts_iqiyi_final = 'http://221.204.187.28/videos/v0/20211108/f0/7f/f5044914a4b82672d7d7411d4e137a5e.265ts?key=087fad6cbd0438193c8cbf32d0d3e14ee&dis_k=2f14cc30a9db5c88498a8fbdd16b5126d&dis_t=1636520905&dis_dz=CNC-Shan3Xi_XiAn&dis_st=139&src=iqiyi.com&dis_hit=0&dis_tag=01210000&uuid=71c8ae08-618b53c9-185&br=100&contentlength=6546160&qd_tm=1636520863838&qd_uid=2210438980839424&qd_k=a0b909a3b922dec5c64f0f3d0cc63916&end=6546160&qd_tvid=2267422040346800&start=0&qd_p=71c8ae08&qyid=4b9036fe9e16710ba22d27800e5b5256&bid=800&qd_index=vod&qd_src=03020031010000000000&sd=0&qd_vip=1&qd_vipres=2&z=taiyuan7_cnc'

# a = time.time()
# res_iqiyi_final_url = requests.get(url=ts_iqiyi_final, proxies={}, stream=True)
# with open(os.path.join('C:/Users/My computer/桌面', '2.ts'), 'wb') as f:
#     for chunk in res_iqiyi_final_url.iter_content(chunk_size=1024):
#         f.write(chunk)
# b = time.time()
# print(f"Use final url! spent: {(b-a):06.3f}")

# a = time.time()
# res_iqiyi_manual_final_url = requests.head(
#     url=ts_iqiyi_direct, proxies={}, allow_redirects=False)
# rear_url = ts_iqiyi_direct
# while res_iqiyi_manual_final_url.status_code == 302:
#     rear_url = res_iqiyi_manual_final_url.headers.get('location')
#     res_iqiyi_manual_final_url.close()
#     res_iqiyi_manual_final_url = requests.head(
#         url=rear_url, proxies={}, allow_redirects=False)
# res_iqiyi_manual_final_url = requests.get(
#     url=rear_url, proxies={}, stream=True)
# with open(os.path.join('C:/Users/My computer/桌面', '3.ts'), 'wb') as f:
#     for chunk in res_iqiyi_manual_final_url.iter_content(chunk_size=1024):
#         f.write(chunk)
# b = time.time()
# print(f"manually finding real url! spent: {(b-a):06.3f}")

# a = time.time()
# res_iqiyi_redirect = requests.get(
#     url=ts_iqiyi_direct, proxies={}, allow_redirects=True, stream=True)
# with open(os.path.join('C:/Users/My computer/桌面', '1.ts'), 'wb') as f:
#     for chunk in res_iqiyi_redirect.iter_content(chunk_size=1024):
#         f.write(chunk)
# b = time.time()
# print(f"Use True setting! spent: {(b-a):06.3f}")

# print(1)

# same target: 6546160  bytes, different step (1,2,3) (3,1,2)
''' 
(1,2,3)
Use default setting! spent: 51.524
Use final url! spent: 02.268
manually finding real url! spent: 04.106 
(3,1,2)
manually finding real url! spent: 35.361
Use default setting! spent: 02.990
Use final url! spent: 01.884 
(2,3,1)
Use final url! spent: 01.887
manually finding real url! spent: 04.018
Use default setting! spent: 02.963
'''

# different target. only one mode (manual, True setting) is proceeding while programe runing
"""
Use True setting! spent: 02.735. size 4737412  bytes
Use True setting! spent: 02.620. size 4737412  bytes
Use True setting! spent: 03.120. size 6146472  bytes
Use True setting! spent: 02.897. size 6146472  bytes

manually finding real url! spent: 04.579. size 6146472  bytes
manually finding real url! spent: 03.582. size 4737412  bytes
manually finding real url! spent: 19.976. size 6146472  bytes
manually finding real url! spent: 34.649. size 4737412  bytes
"""

# (Wrong!) Conclusion: real url(in default mode) > True > manual
#   1: you should use True mode in MultipleThreadDownloader, cause you can get the real url. Even though you have gotten the url which will be redirect, True mode will always be good choice.
#   2:
# allow_redirects = True will lost Referen.
# 4
# 813.05 seconds
''' headers = headers = {
    'User-Agent': 'QYPlayer/Android/4.4.5;NetType/3G;QTP/1.1.4.3',  # !
    'Accept-Encoding': '*'
} '''
""" headers = headers = {
    'User-Agent': 'QYPlayer/Android/4.4.5;NetType/3G;QTP/1.1.4.3',  # !
    'Accept-Encoding': '*',
    'Connection': 'Keep-Alive',
    'Range': 'bytes=0-0',
}
root = tkinter.Tk()
root.withdraw()

m3u8 = filedialog.askopenfilename()
save_path = filedialog.askdirectory()
play_list = []
with open(m3u8, 'r') as f:
    all_content = f.read().split("\n")
with open(os.path.join(save_path, 'play.txt'), 'w') as f:
    for index, line in enumerate(all_content):
        # get real url
        if "#EXTINF" in line:
            play_list.append(all_content[index + 1])
            f.write(all_content[index + 1])
start_time = time.time()
for url in play_list:
    a = time.time()
    # res = requests.head(url=url,headers=headers,allow_redirects=False,proxies={},stream=True)
    res = requests.get(url=url,headers=headers,allow_redirects=False,proxies={},stream=True)
    while(res.status_code == 302):
        url = res.headers.get('location')
        # res.close()
        # res = requests.head(url=url,headers=headers,allow_redirects=False,proxies={},stream=True)
        res = requests.get(url=url,headers=headers,allow_redirects=False,proxies={},stream=True)
    b = time.time()
    print(f"{(b-a):05.3f} seconds, size {res.headers.get('Content-Length')}")
end_time = time.time()
print(f"{(end_time-start_time):05.2f} seconds")
 """