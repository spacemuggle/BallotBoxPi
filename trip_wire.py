import RPi.GPIO as GPIO
import time

# set mode
GPIO.setmode(GPIO.BOARD)
# pins used for input and output
outs = [11,13]
ins = [5,7]
# setup input and output pins
GPIO.setup(outs, GPIO.OUT)
GPIO.setup(ins, GPIO.IN) # sensors read 1 for dark and 0 for light

# make sure inital input reads low
def sensor_check(ins):    
    issue = False
    for pin in outs:
        if GPIO.input(pin) == False:
            issue = True
    if issue == True:
        msg = "Move to darker area or adjust sensor sensitivity."
        print(msg)
    # return true if test passes, false ow
    return(not issue)

# run sensor check
pass_test = sensor_check(ins)

# Turn on lasers
GPIO.output(outs, GPIO.HIGH)

# create input callback
def trip_action(channel):
    GPIO.output([11,13], GPIO.LOW)
    time.sleep(2)
    GPIO.output([11,13], GPIO.HIGH)

# set up event detection
for pin in ins:
    GPIO.add_event_detect(pin, GPIO.FALLING, callback = trip_action,
                      bouncetime = 200)

time.sleep(60)

GPIO.cleanup()
