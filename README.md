# BallotBoxPi
Project to turn raspberry pi into a laser trip sensor that plays a random sound when the laser is tripped. This is intended as use on the inside of a ballot box so sound is played when a ballot is dropped in.

## Goals:

- [X] Auto detect flash-drive and mount to known location.
- [x] Get audio files (.mp3 & .wav) and volume from a volume.txt file.
- [x] Create script to calibrate and montitor laser sensors for "trip".
- [x] Write function that plays a random sound.
- [ ] Determine method for attaching bluetooth speakers without screen.
- [ ] Add shutdown button.

## Notes:

* Created sensor array frame (https://www.thingiverse.com/thing:4444818)
* Flattened program to single file "BallotBoxPi.py"
* Added autostart using systemd following this [documentation](https://www.raspberrypi.org/documentation/linux/usage/systemd.md)
* Need to find way to allow autostart to pull from flashdrive properly
