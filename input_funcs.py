# assuming drive auto mounted and location is known
import os, shutil

########################################################
# function to check if path or list of paths are all dirs
def CheckDirsExist(paths):
    '''Checks if dir or dirs exist, returns false if at least 1 DNE'''
    if type(paths) == list:            
        for p in paths:
            if not os.path.isdir(p):
                return(False)
        return(True)
    elif type(paths) == str:
        if not os.path.isdir(paths):
            return(False)
        return(True)
    else:
        return('wrong type')

# # test function usability
# abc = ['a', 'b', 'c']
# a = 'b'
# checkabc = CheckDirsExist(abc)
# checka = CheckDirsExist(a)
# it works, I think, didn't do extensive testing

########################################################
# function that checks if two directories hold the same file names
# (will not detect changes to files that keep the same names aka volume)
def NewFileCheck(new_p, old_p):
    '''Check if two dirs have same files (ignores dirs)'''
    # if target dest for new files DNE, return True
    if not os.path.isdir(old_p):
        return(True)
    # if source dest for comparing files DNE, return False
    if not os.path.isdir(new_p):
        return(False)
    # get directory contents as list
    new_files = os.listdir(new_p)
    old_files = os.listdir(old_p)
    # store lists as iterable
    file_lists = [new_files, old_files]
    # remove anything that is not a file from lists
    for files in file_lists:    
        for fname in files:
            full_path = os.path.join(new_p, fname)
            if not os.path.isfile(full_path):
                files.remove(fname)
        # sort lists for comparing
        files.sort()
    # compare lists (return True for differences)
    return(new_files != old_files)
    
# # test function usability
# p_n = "/media/pi/MP3'S"
# p_o = "/home/pi/Documents/Projects/BallotBoxPi/sounds"
# new_file = NewFileCheck(new_p = p_n, old_p = p_o)
# print(new_file)
# # it works! passes True if difference is found and False ow

########################################################
# function to delete files so new ones can go in
# deletes every file in the directory but not the dir
def DeleteDirFiles(loc):
    '''Deletes all files in given dir but leaves dir'''
    # check if directory path exists, exit if it doesn't
    if not os.path.isdir(loc):
        print("couldn't delete files, dir loc DNE")
        return
    # get files in directory
    files = os.listdir(loc)
    # delete each file
    for file in files:
        full_path = os.path.join(loc, file)
        os.remove(full_path)
    
# # test function usability
# dirloc = "/home/pi/Documents/Projects/BallotBoxPi/sounds"
# DeleteDirFiles(loc = dirloc)
# # works as intended!!! Deletes all files within the dir without
# # deleting the dir

########################################################
# checks if any files exist in loc dir
# returns True if dir is empty and False ow
def CheckEmpty(loc):
    '''Checks if any files exist in given dir'''
    if len(os.listdir(loc)) == 0:
        return(True)
    else:
        return(False)

# # test function usability
# dirloc = "/media/pi/MP3'S"
# # works as inteded!

########################################################
# copy all files(list) and no folders from orig(str) to dest(str)
def CopyFiles(orig, dest):
    '''Copy all files from one dir to another dir (ignores subdirs)'''
    # check if dest exists
    if os.path.exists(dest):
        msg = 'existing dest directory used'
    else:
        msg = 'new dest directory created'
        # create directory
        os.mkdir(dest)
    # Do copy procedure #
    # get files from orig
    files = os.listdir(orig)
    for file in files:
        # check if file
        orig_p = os.path.join(orig, file)
        if os.path.isfile(orig_p):
            # copy file
            dest_p = os.path.join(dest, file)
            shutil.copyfile(orig_p, dest_p)
        else:
            # ignore directories
            pass
    # tell user if new or existing directory was used
    print(msg)

# # test function usability (writes over same name files)
# fr = "/media/pi/MP3'S"
# to = "/home/pi/Documents/Projects/BallotBoxPi/sounds"
# f_list = os.listdir(fr)
# CopyFiles(orig = fr, dest = to, files = f_list)

#########################################################
# pull out fpaths to sounds as list and volume as int var
# (defaults volume to 100 if issue occurs)
def OrgInputData(loc):
    '''Formats data and returns(sounds, volume)'''
    sounds = []
    volume = 100
    files = os.listdir(loc)
    for file in files:
        # store full file path
        full_path = os.path.join(loc, file)
        # store .wav and .mp3 fpaths in sounds
        if file.endswith('.wav') or file.endswith('.mp3'):
            sounds.append(full_path)
        # pull volume from .txt file
        # (works on any fname containing "vol")
        elif file.endswith('.txt'):
            if 'vol' in file.lower():
                volume = open(full_path, 'r').readline()
                # check if number was pulled
                try:
                    volume = int(volume)
                    # check if valid number
                    if volume < 0 or volume > 100:
                        volume = 100
                except:
                    volume = 100
    return(sounds, volume)

# # test function usability
# loc_f = "/home/pi/Documents/Projects/BallotBoxPi/sounds"
# sounds, volume = OrgInputData(loc = loc_f)
# # works as intended!