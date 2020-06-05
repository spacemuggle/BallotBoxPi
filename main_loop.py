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
        print(f"start trip\nlen sounds: {len(sounds)}\nlen recent: {len(recent)}")
        sound = aplay.choose_sound(sounds)
        while sound in recent:
            sound = aplay.choose_sound(sounds)
        # play the new sound
        aplay.play_sound(sound)
        # record sound as recently played
        recent.append(sound)
        # remove first item in recently played
        recent.remove(recent[0])
        return(recent)

    # start event detection
    for pin in ins:
        GPIO.add_event_detect(pin, GPIO.RISING,
                              bouncetime = 250)
    
    ################################################## 
    # start infinite loop
    ##################################################
    recent = [""] * 5
    while True:
        time.sleep(0.05)
        for pin in ins:
            if GPIO.event_detected(pin):
                GPIO.remove_event_detect(pin)
                recent = trip_action(recent, sounds)
                GPIO.add_event_detect(pin, GPIO.RISING,
                                      bouncetime=250)
        
# ensure cleanup occurs
finally:    
    # cleanup GPIO
    GPIO.cleanup()