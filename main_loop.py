import aplay_sound as aplay
import RPi.GPIO as GPIO
import time, setup_files

#################################################
# set up try/finally to ensure cleanup occurs ###
#################################################
try:
    #################################################
    # bring in sounds from setup_files.py
    #################################################
    sounds = setup_files.sounds

    #################################################
    # set up inputs/ outputs and turn on lasers #####
    #################################################
    # set mode
    GPIO.setmode(GPIO.BOARD)
    # pins used for input and output
    outs = [11,13] # lasers
    ins = [5,7] # light sensors
    # setup input and output pins
    GPIO.setup(outs, GPIO.OUT)
    GPIO.setup(ins, GPIO.IN) # sensors read 1 for dark and 0 for light
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
    # run sensor check
    pass_test = sensor_check(ins)
    # turn on lasers if pass, blink lasers if fail
    if pass_test == True:
        GPIO.output(outs, GPIO.HIGH)
    else:
        for i in range(20):
            GPIO.output(outs, not GPIO.input(outs[0]))
            time.sleep(1)

    #################################################
    # create callback function/ start event detection
    #################################################
    # create input callback
    def trip_action(recent, sounds):
        # if sound was recently played, pick a new one
        sound = aplay.choose_sound(sounds)
        while sound in recent:
            sound = aplay.choose_sound(sounds)
        # exit early if only one sound exists
        if len(sounds) == 1:
            return(recent)
        # play the new sound
        aplay.play_sound(sound)
        # record sound as recently played
        recent.append(sound)
        # remove first item in recently played
        recent.remove(recent[0])
        return(recent)
    
    # initialize recent array (handles only 1 sound edge case)
    recent = [""] * (int(len(sounds)/2.01) + 1)

    # start event detection
    def start_detection(pins):
        for pin in pins:
            GPIO.add_event_detect(pin, GPIO.RISING,
                                  bouncetime = 250)

    # end event detection
    def end_detection(pins):
        for pin in pins:
            GPIO.remove_event_detect(pin)

    # start initial event detection
    start_detection(ins)

    ##################################################
    # start infinite loop
    ##################################################
#    i = 0
    while True:
        time.sleep(0.05)
#        i += 1
        for pin in ins:
            if GPIO.event_detected(pin):
                end_detection(ins)
                recent = trip_action(recent, sounds)
                start_detection(ins)
#        if i > 1000:
            break
# ensure cleanup occurs
finally:
    # cleanup GPIO
    GPIO.cleanup()
