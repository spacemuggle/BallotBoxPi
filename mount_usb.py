import os, subprocess

# create mount directory
mount_loc = "/media/usb-drive"
subprocess.run(["sudo","mkdir","-p",mount_loc])

# mount USB drive
usb_loc = "/dev/sda1"
subprocess.run(["sudo","mount",usb_loc,mount_loc])