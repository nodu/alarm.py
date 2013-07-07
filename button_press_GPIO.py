#!/usr/bin/env python

# Matt Nodurfth
#Button wiriting: Bottom Left GND, Top Right Pin 23 and 10k resistor, 10k Resistor goes inbetween 3.3V and tied with 23

# Add buttonPressGPIO.py to startup
# Some sources suggest adding to rc.local isn't a best practice.  I'm looking into daemonizing the process
# python /home/pi/.mpd/alarm.py/button_press_GPIO.py >> /home/pi/.mpd/alarm.py/button.log 2>&1 &

#from time import sleep
import time
import re, commands, RPi.GPIO as GPIO # Should get used to using subprocess as commands is depricated
import mpd_alarm as alarm

state_list = [ 'mpc clear', 'mpc volume 100' , 'mpc repeat off', 'mpc random off', 'mpc single off', 'mpc consume off']

GPIO.setmode(GPIO.BCM) # Sets the pin layout to BCM 
GPIO.setup(23, GPIO.IN) # Init varible for GPIO BCM pin 23 as input
button_press_length = 0 # Init varible

def check_state():
    (status, output) = commands.getstatusoutput('mpc status')
    output_match = re.search(r'\[(\w+)\]', output)
    return output_match
print "This ish is starting -- ", time.strftime("%a, %d %b %Y %H:%M:%S")
while True:
    input = GPIO.input(23)
    if input == False: #change the wiring of the switch and change back to True, or keep as is... WORKING False
        if button_press_length == 0:
            print "pressed!"
            if check_state() == None:(status3, output3) = commands.getstatusoutput('mpc play')
            elif check_state().group(1) == 'playing':
                (status1, output1) = commands.getstatusoutput('mpc pause')
            else: (status2, output2) = commands.getstatusoutput('mpc play')
        elif button_press_length > 3: # Still outputs a press of length 0 before printing the long press, need to prevent the first length 0 press..
            print "You pressed the button for longer than 3 seconds!"
            alarm.set_state(state_list)
            alarm.add_random_playlist()
            alarm.start_mpd()
            button_press_length = 0
        
        button_press_length += 0.05        
    else:
        button_press_length = 0
    
    prev_input =  not input
    time.sleep(0.05) # Prevents debounching
    
    
#It's not recording the presses in the log started by rc.local...