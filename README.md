# BallotBoxPi
This code turns a raspberry pi into a dual laser trip sensor that plays a random sound when a laser is tripped. This is intended as use on the inside of a ballot box so sound is played when a ballot is dropped in.

### Warning!!!
**This is an inherently fragile system running an operating system off a microSD. Please never unplug the device during bootup or if the green light on the pi is flickering. Starting up can take up to 30-45 seconds when you plug it in so please be patient.**
**Since this runs entirely off the microSD, make sure not to damage the sd card. Always remove the card before taking the pi out of its case**

### Usage:

* First use - Power it on by plugging in the supplied power supply. Plug in some speakers to the aux and it should work with the built in sounds.

* Changing sounds - Get a flashdrive and name it "MP3". **No other name is accepted, if you do not name it that the drive will be ignored**. Add as many .mp3 and .wav files as you want and plug it into the pi. Make sure it is running when you plug it in. Once the lasers stop blinking you should be good to go. You can now remove the drive.

* Changing volume - On the MP3 flashdrive, create a new text file named volume.txt. In this file put the desired volume as a number 0-100 and nothing else. The default setting if no volume file exists is 100.

* Changing sound duration - If the sounds are cutting off before you want them too or going on for too long, you can adjust this value. The default value is 5 seconds. To change it, add a file named maxtime.txt to the MP3 drive with the max amount of seconds you want a sound to play for and nothing else.

* Notes - Whenever a drive is plugged in it will delete the local files and copy over all the files in case a setting has changed. If you plug in an empty drive named MP3 it will **delete all the music**. Make sure if you are changing the volume or maxtime that the sounds on the drive are the sounds you want on the pi. You can keep the drive in the pi if you want but it will slightly slow down the startup.

* For troubleshooting and more detailed information, check out the [wiki](https://github.com/spacemuggle/BallotBoxPi/wiki)!

## Notes:

* To connect bluetooth speakers you can follow this [tutorial](https://pimylifeup.com/raspberry-pi-bluetooth/)
* Created sensor array frame (https://www.thingiverse.com/thing:4444818)
* Added autostart using systemd following this [documentation](https://www.raspberrypi.org/documentation/linux/usage/systemd.md)
* Code restarts on flashdrive plugin or unplug
