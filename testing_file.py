import get_usb_files, subprocess, os
import random as rnd
from pygame import mixer
import play_rand_sound as prs

#bring in sounds and volume setting from USB
max_volume = get_usb_files.max_vol
sound_paths = get_usb_files.sounds

#set audio volume & initialize audio mixer