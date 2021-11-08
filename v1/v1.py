import os
import subprocess


def check_vedio_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in set(['mkv', 'mp4'])

def get_media_info(file, save_path):
    command = 'mediainfo ' + file + ' | tee ' + save_path + "info.txt"
    print(command)
    result = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE).stdout
    result.readlines()
    return 
def creat_image_contract_sheet(video_file, save_path):
    command = "bash " + "/home/pi/vcs.bash " + \
        video_file + " " + image_config + " -o " + save_path + "imagesheet.jpg"
    
    os.system(command)

def creat_torrent(dir_path, save_path, name):
    command = "mktorrent  -l 22 -p -v -o " + save_path + name + " " + dir_path
    os.system(command)

if (__name__ == '__main__'):
    #dir_path = "/home/pi/DiskShare/Film/We.Made.a.Beautiful.Bouquet.2021.1080p.BluRay.x264.DTS-WiKi/"
    dir_path = input("\n input video file path \n")
    image_config = "-U0 -n 12 -c 4 -H 200 -a 300/200"
    save_path = "/home/pi/share/mh/torrent/AutoPush/"
    

    file_path = ""
    name = ""
    for i in os.listdir(dir_path):
        if check_vedio_file(i):
            file_path = os.path.join(dir_path, i)
            name = i.rsplit('.', 1)[0]
            save_path = os.path.join(save_path, i.rsplit('.', 1)[0]) + "/"
            break
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    get_media_info(file_path, save_path)
    creat_image_contract_sheet(file_path, save_path)
    creat_torrent(dir_path, save_path, name)
