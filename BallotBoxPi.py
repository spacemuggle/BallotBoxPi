#################################################
#################################################
# set path to USB and Local directory
#################################################
#################################################
USB_dir = "/media/pi/MP3"
Loc_dir = "/home/pi/Coding/Projects/BallotBoxPi/sounds"

#################################################
#################################################
# do all imports
#################################################
#################################################
import RPi.GPIO as GPIO
import random as rnd
from pydub import AudioSegment
import os, math, time, shutil

#################################################
#################################################
# set up functions
#################################################
#################################################

# logger function
from functools import wraps

log_file = '/home/pi/Coding/Projects/BallotBoxPi/bbp_run.log'
# clear log
with open(log_file, 'w+') as f:
    f.write('')

def my_logger(original_func):
    import logging
    logging.basicConfig(filename=f'{log_file}',
                        level=logging.INFO)

    @wraps(original_func)
    def wrapper(*args, **kwargs):
        result = original_func(*args, **kwargs)
        logging.info(f'{original_func.__name__} ran with {args} & {kwargs}\n resulting in {result}')
        return original_func(*args, **kwargs)

    return wrapper

# aplay sound funcs
#################################################
def choose_sound(sounds):
    #get rand sound
    rand_sound = int(round((len(sounds)-1) * rnd.random(), 0))
    sound = sounds[rand_sound]
    return(sound)

def set_volume(volume):
    # convert sound to get desired output sound
    if volume > 2: # 
        volume = round(math.log(volume, 1.041616) - 13)
    # set volume
    devices = ["PCM", "Master", "Speaker", "Headphone"]
    for dev in devices:
        os.system(f'amixer set {dev} unmute')
        os.system(f'amixer set {dev} {volume}%')

def play_sound(sound, max_time):
    # play sound through set output, return sound path
    os.system(f'aplay -q -d {max_time} {sound}')
    return(sound)

# input functions
#################################################
# function to check if path or list of paths are all dirs
@my_logger
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

# checks if any files exist in loc dir
# returns True if dir is empty and False ow
@my_logger
def CheckEmpty(loc):
    '''Checks if any files exist in given dir'''
    try:
        if len(os.listdir(loc)) == 0:
            return(True)
        else:
            return(False)
    except:
        return(True)

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

# converts mp3 files to wav and deletes original mp3
def mp3_2_wav(file, copy=False):
    path, ext = os.path.splitext(file)
    ext = '.wav'
    src = file
    dst = path + ext
    snd = AudioSegment.from_mp3(src)
    snd.export(dst, format = "wav")
    # delete MP3
    if copy==False:
        os.remove(file)

# pull out sound paths as list, volume as int, max time as int
# (defaults: volume = 100, max_time = 5)
@my_logger
def OrgInputData(loc):
    '''Formats data and returns(sounds, volume)'''
    sounds = []
    volume = 100
    max_time = 5
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
                try: # try to read first line of file
                    with open(full_path, 'r') as f:
                        volume = f.readline()
                    # ensure valid input
                    volume = int(volume)
                    if volume < 0 or volume > 100:
                        volume = 100
                except:
                    volume = 100
            elif 'time' in file.lower():
                try: # try to read first line of file
                    with open(full_path, 'r') as f:
                        max_time = f.readline()
                    # ensure valid input
                    max_time = int(max_time)
                    if max_time < 1 or max_time > 100:
                        max_time = 5
                except:
                    max_time = 5
    return(sounds, volume, max_time)

# GPIO functions
#################################################
# make sure inital input reads low
def sensor_check(ins):
    issue = False
    for pin in ins:
        if GPIO.input(pin) == False:
            issue = True
    if issue == True:
        msg = "Move to darker area or adjust sensor sensitivity."
        print(msg)
    # return true if test passes, false ow
    return(not issue)

# create function for action to take when event is detected
def trip_action(recent, sounds, max_time):
    # if sound was recently played, pick a new one
    sound = choose_sound(sounds)
    while sound in recent:
        sound = choose_sound(sounds)
    # exit early if only one sound exists
    if len(sounds) == 1:
        return(recent)
    # play the new sound
    play_sound(sound, max_time)
    # record sound as recently played
    recent.append(sound)
    # remove first item in recently played
    recent.remove(recent[0])
    return(recent)

# start event detection
def start_detection(pins):
    for pin in pins:
        GPIO.add_event_detect(pin, GPIO.RISING,
                                bouncetime = 250)

# end event detection
def end_detection(pins):
    for pin in pins:
        GPIO.remove_event_detect(pin)

#################################################
#################################################
# setup the files and get user inputs
#################################################
#################################################
# Determine exists for both dirs
USB_exist = CheckDirsExist(USB_dir)
Loc_exist = CheckDirsExist(Loc_dir)

# Imply empty to mean empty or DNE
USB_empty, Loc_empty = True, True
if USB_exist:
    USB_empty = CheckEmpty(USB_dir)
if Loc_exist:
    Loc_empty = CheckEmpty(Loc_dir)

# Case 0: USB DNE or empty & Local dir DNE or empty
#        >print error
if USB_empty and Loc_empty:
    print('No files found in local directory or USB directory')
# Case 1: USB DNE or empty & Local dir nonempty
#        >default to existing files (do nothing)
elif USB_empty and (not Loc_empty):
    print('USB empty or DNE, defaulting to existing files')
# Case 2: USB files nonempty
#        >delete local files and copy in new files
elif not USB_empty:
    print('USB found, copying files in')
    if not Loc_empty:
        DeleteDirFiles(Loc_dir)
    CopyFiles(orig = USB_dir, dest = Loc_dir)
    print('copy complete')

# Get full paths to sounds and the volume as an int(0,100)
sounds, volume, max_time = OrgInputData(Loc_dir)

# Set system volume
set_volume(volume)

#################################################
# write some more info to the log file
with open(log_file, 'a') as f:
    lines = [f'\nUSB_exist : {USB_exist} ', f'\nUSB_empty : {USB_empty} ',
             f'\nLoc_exist : {Loc_exist} ', f'\nLoc_empty : {Loc_empty}']
    f.writelines(lines)

#################################################
#################################################
# set up try/finally to ensure cleanup occurs
#################################################
#################################################
try:
    # set up inputs/ outputs and turn on lasers
    #################################################
    # set mode
    GPIO.setmode(GPIO.BOARD)
    # pins used for input and output
    outs = [11,13] # lasers
    ins = [5,7] # light sensors
    # setup input and output pins
    GPIO.setup(outs, GPIO.OUT)
    GPIO.setup(ins, GPIO.IN) # sensors read 1 for dark and 0 for light
    # run sensor check
    pass_test = sensor_check(ins)
    # turn on lasers if pass, blink lasers if fail
    if pass_test == True:
        GPIO.output(outs, GPIO.HIGH)
    else:
        for i in range(20):
            GPIO.output(outs, not GPIO.input(outs[0]))
            time.sleep(1)

    # start event detection/ init recent array
    #################################################    
    # initialize recent array (handles only 1 sound edge case)
    recent = [""] * (int(len(sounds)/2.01) + 1)
    # start initial event detection
    start_detection(ins)

    # start infinite loop
    ##################################################
    while True:
        time.sleep(0.05)
        for pin in ins:
            if GPIO.event_detected(pin):
                end_detection(ins)
                recent = trip_action(recent, sounds, max_time)
                start_detection(ins)
            break
# ensure cleanup occurs
finally:
    # cleanup GPIO
    GPIO.cleanup()