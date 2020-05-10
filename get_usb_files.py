import os, subprocess

#create mount directory
mount_loc = "/media/usb-drive"
subprocess.run(["sudo","mkdir","-p",mount_loc])
#mount USB drive
usb_loc = "/dev/sda1"
subprocess.run(["sudo","mount",usb_loc,mount_loc])

##drive location
#base_path = os.fspath("/media")

#drive_name = os.listdir(base_path) #1 item list (if nothing else plugged in)
#drive_path = os.path.join(base_path, drive_name[0]) #store path to usb
drive_path = mount_loc

#function returns list of file paths to sounds and max volume
#if no .txt file or if error, set max_volume to 10
def OrganizeInputFiles(d_path):
    sounds = []
    max_vol = 10
    files = os.listdir(d_path)
    for file in files:
        name, ext = os.path.splitext(file)
        filepath = os.path.join(d_path, name + ext)
        if ext == '.mp3' or ext == '.wav':
            sounds.append(filepath)
        elif ext =='.txt':
            try:
                #print(os.path.join(d_path, name + ext))
                vol_file = open(os.path.join(d_path, name + ext), 'r')
                max_vol = vol_file.readlines()
                max_vol = int(max_vol[0])
                if max_vol < 0 or max_vol > 10:
                    max_vol = 10
            except:
                pass
    return(sounds, max_vol)

sounds, max_vol = OrganizeInputFiles(d_path=drive_path)