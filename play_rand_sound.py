sound_file_paths = ["/media/pi/MP3'S/517058__invisible-inks__scifi-sniper-rifle.wav",
                    "/media/pi/MP3'S/178817__felfa__dtmf-dial.mp3",
                    "/media/pi/MP3'S/484058__subtletransmissions__lazer-3.wav",
                    "/media/pi/MP3'S/516245__wyronroberth__drop-tool.mp3",
                    "/media/pi/MP3'S/425556__planetronik__rock-808-beat.mp3",
                    "/media/pi/MP3'S/516854__robinhood76__08687-shine-magic-stinger.wav"]


import random as rnd
import subprocess, vlc
#from pygame import mixer, time #can handle WAV, MP3, or OGG files

def choose_sound(sounds):
    #get rand sound
    rand_sound = rnd.choice(sounds)
    return(rand_sound)


def play_sound(max_volume, sound):
    #set audio volume
    subprocess.run(['amixer', 'set', 'PCM', 'unmute'])
    subprocess.run(['amixer', 'set', 'PCM', '{}%'.format(max_volume*10)])
    #initialize vlc instance
    instance = vlc.Instance('--aout=alsa')
    p = instance.media_player_new()
    m = instance.media_new(sound)
    p.set_media(m)
    vlc.libvlc_audio_set_volume(p, max_volume)
    p.play()

rnd_sound = choose_sound(sounds=sound_file_paths)
play_sound(max_volume=100, sound=rnd_sound)

#instance = vlc.Instance('--aout=alsa')
#p = instance.media_player_new()
#m = instance.media_new("/media/pi/MP3'S/517058__invisible-inks__scifi-sniper-rifle.wav")
#p.set_media(m)
#p.play()
#vlc.libvlc_audio_set_volume(p, 100)