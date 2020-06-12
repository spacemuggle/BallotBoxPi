# BallotBoxPi
Project to turn raspberry pi into a laser trip sensor that plays a random sound when the laser is tripped. This is intended as use on the inside of a ballot box so sound is played when a ballot is dropped in.

## Goals:

- [ ] Auto detect flash-drive and mount to known location.
- [x] Get audio files (.mp3 & .wav) and volume from a volume.txt file.
- [x] Create script to calibrate and montitor laser sensors for "trip".
- [x] Write function that plays a random sound.
- [ ] Determine method for attaching bluetooth speakers without screen.
- [ ] Add shutdown button.

## Notes:

* Created sensor array frame (https://www.thingiverse.com/thing:4444818)
* Functional prototype code runs in main_loop.py (reliant on other files to work)
