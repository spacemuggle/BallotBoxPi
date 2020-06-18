import os, math
import random as rnd

# sound_path = '/home/pi/Documents/Projects/BallotBoxPi/sounds/lazer3.wav'
# os.system('aplay ' + sound_path)
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
    os.system(f'aplay -q -d {max_time} {sound}')
    return(sound)