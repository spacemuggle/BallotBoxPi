# assuming drive auto mounted and location is known
import os, shutil

########################################################
# function to check if path or list of paths are all dirs
def CheckDirsExist(paths):
    '''Checks if dir or dirs exist, returns false if at least 1 DNE'''
    if type(paths) == list:
        for p in paths:
            try:
                if not os.path.isdir(p):
                    return(False)
                else:
                    return(True)
            except:
                return(False)
    elif type(paths) == str:
        try:
            if not os.path.isdir(paths):
                return(False)
            else:
                return(True)
        except:
            return(False)
    else:
        return('wrong type')

# # test function usability
# abc = ['a', 'b', 'c']
# a = 'b'
# checkabc = CheckDirsExist(abc)
# checka = CheckDirsExist(a)
# it works, I think, didn't do extensive testing

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
    try:
        if len(os.listdir(loc)) == 0:
            return(True)
        else:
            return(False)
    except:
        return(True)
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
# function to convert mp3 to wav

# # sudo pip3 install pydub # at command line
# from pydub import AudioSegment
# 
# testmp3 = "/media/pi/MP3'S/felfa.mp3"
# dest = "/media/pi/MP3'S/felfa.wav"
# 
# snd = AudioSegment.from_mp3(testmp3)
# snd.export(dest, format="wav")
from pydub import AudioSegment

def mp3_2_wav(file):
    path, ext = os.path.splitext(file)
    ext = '.wav'
    src = file
    dst = path + ext
    snd = AudioSegment.from_mp3(src)
    snd.export(dst, format = "wav")
    # delete MP3
    os.remove(file)
    
    
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
        # convert mp3 to wav
        if file.endswith('.mp3'):
            mp3_2_wav(full_path)
            wav_path = os.path.splitext(full_path)[0] + '.wav'
            sounds.append(wav_path)
        # store wav to sounds list
        if file.endswith('.wav'):
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
        
