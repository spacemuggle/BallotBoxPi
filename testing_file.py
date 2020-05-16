import input_funcs as ifns

# set USB and Local file locations
USB_dir = "/media/pi/MP3'S"
Loc_dir = "/home/pi/Documents/Projects/BallotBoxPi/sounds"

# Determine exists for both dirs
USB_exist = ifns.CheckDirsExist(USB_dir)
Loc_exist = ifns.CheckDirsExist(Loc_dir)

# Imply empty to mean empty or DNE
USB_empty, Loc_empty = True, True
if USB_exist:
    USB_empty = ifns.CheckEmpty(USB_dir)
if Loc_exist:
    Loc_empty = ifns.CheckEmpty(USB_dir)

# Case 0: USB DNE or empty & Local dir DNE or empty
#        >print error
if USB_empty and Loc_empty:
    print('No files found in local directory or USB directory')
# Case 1: USB DNE or empty & Local dir nonempty
#        >default to existing files (do nothing)
elif USB_empty and (not Loc_empty):
    pass
# Case 2: USB files nonempty
#        >delete local files and copy in new files
elif not USB_empty:
    if not Loc_empty:
        ifns.DeleteDirFiles(Loc_dir)
    ifns.CopyFiles(orig = USB_dir, dest = Loc_dir)

# Get full paths to sounds and the volume as an int(0,100)
sounds, volume = ifns.OrgInputData(Loc_dir)
###################################################
# Not currently working, need to create function
# for main input stream handling and build overarching
# if statement into seperate function.
# then consider if there is a good way to combine this
# with the contents of input_funcs.py to avoid import
# complexity