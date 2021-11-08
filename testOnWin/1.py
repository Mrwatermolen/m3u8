import tkinter
from tkinter import filedialog
from multipleThreadDownloader import MultipleThreadDownloader


def download_from_playlist(playlist, save_path, start_line=None, end_line=None, cryptor=None):

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
download_from_playlist(list, save, 60)
