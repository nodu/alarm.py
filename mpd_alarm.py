#!/usr/bin/python
# Uses mpd and mpc to play a random playlist starting at 6:35AM with increasing volume.
# Matt Nodurfth

# Setup: Add this python script to a cron with your desired start time, path can be anywhere
# 35 6 * * 1-5 /home/pi/.mpd/alarm.py To start at 6:35AM M-F
# Change varibles based on your directory structure and desired increments

# Add a script to add this program to crontab?

import os, time, commands, random, sys, re

playlist_dir = '/home/pi/.mpd/playlists'
alarm_log = '/home/pi/.mpd/alarm.py/mpd_alarm.log' 
mpd_volume = 60 # Initial volume setting
step_vol = 10 # Increase volume by 10%
step_increment = 150 # Increases volume every 150 seconds

# Sets the initial state of MPD.  Clears the playlist; sets volume; and turns repeat, random, single, and consume off
state_list = [ 'mpc clear', 'mpc volume ' + str(mpd_volume), 'mpc repeat off', 'mpc random off', 'mpc single off', 'mpc consume off']

def log(cmd, status, output):
    """Function for logging errors with timestamp"""
    if status != 0: 
        log = open(alarm_log, 'a')
        log.write(time.strftime("%a, %d %b %Y %H:%M:%S") + ' --  ' + cmd + ': ' + output +'\n')
        log.close()
        
def set_state(state):
    """Set initial state"""
    for cmd in state:
        (status, output) = commands.getstatusoutput(cmd)
        log(cmd, status, output)

def add_random_playlist():
    """Chose a random playlist"""
    cmd = 'mpc load '
    playlist_list = os.listdir(playlist_dir)
    if not playlist_list:
        log('playlist', 1, 'NO PLAYLISTS!!!')
        sys.exit(1)
    random_num = random.choice(playlist_list)
    album_name = re.sub(' ', '\ ', random_num)
    (status, output) = commands.getstatusoutput(cmd + album_name)
    log(cmd, status, output)
    
def start_mpd():
    """Start mpd""" 
    cmd = 'mpc play'
    (status, output) = commands.getstatusoutput(cmd)
    log(cmd, status, output)

def vol_increase(mpd_volume, step_vol, step_increment):
    """Increase volume by 10 every 2.5 minutes"""
    cmd = 'mpc volume'
    while mpd_volume < 101:
        time.sleep(step_increment)
        (status, output) = commands.getstatusoutput('mpc volume ' + str(mpd_volume))
        log(cmd, 0, output)
        mpd_volume += step_vol
        
def main():
    set_state(state_list)
    add_random_playlist()
    start_mpd()
    vol_increase(mpd_volume, step_vol, step_increment)
    sys.exit(0)

if __name__ == '__main__':
    main()