
#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# Olivier Devauchelle, 2021

#-------------------------------------------------------------------------------
# Name:         Shutdown Daemon
#
# Purpose:      This program gets activated at the end of the boot process by
#               cron. (@ reboot sudo python /home/pi/shutdown_daemon.py)
#               It monitors a button press. If the user presses the button, we
#               Halt the Pi, by executing the poweroff command.
#
#               The power to the Pi will then be cut when the Pi has reached the
#               poweroff state (Halt).
#               To activate a gpio pin with the poweroff state, the
#               /boot/config.txt file needs to have :
#               dtoverlay=gpio-poweroff,gpiopin=27
#
# Author:      Paul Versteeg
#
# Created:     15-06-2015, revised on 18-12-2015
# Copyright:   (c) Paul 2015
# https://www.raspberrypi.org/forums/viewtopic.php?p=864409#p864409
#-------------------------------------------------------------------------------

import RPi.GPIO as GPIO
import subprocess
import time
from RadioPlayer import switch_off_radio

GPIO.setmode( GPIO.BCM ) # use GPIO numbering
GPIO.setwarnings( False )

INT = 24    # GPIO button interrupt to shutdown procedure

# use a weak pull_up to create a high
GPIO.setup(INT, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def main():

    while True:
        # set an interrupt on a falling edge and wait for it to happen
        GPIO.wait_for_edge(INT, GPIO.FALLING)

        # subprocess.call(['python3 ampli.py off && killall mplayer'], shell=True, stdout=subprocess.PIPE)
        print('Stopping radio streaming.')
        switch_off_radio()

        time.sleep(1.5)   # Wait 1 second to check for spurious input

        if( GPIO.input(INT) == 0 ) :
            print('Shutdown.')
            subprocess.call(['sudo shutdown -h now'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def run_as_background() :
    subprocess.Popen( [ 'python3', 'button.py'], creationflags=subprocess.DETACHED_PROCESS )
    # subprocess.Popen( [ 'python3', 'button.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE ).communicate()

if __name__ == '__main__' :
    main()
