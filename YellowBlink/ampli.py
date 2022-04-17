
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

import sys
import RPi.GPIO as GPIO

GPIO.setmode( GPIO.BCM )
GPIO.setwarnings( False )

##############################

pin_number = 17

GPIO.setup( pin_number, GPIO.OUT )

##############################

def ampli_control( switch ) :

    if switch == 'on' :
        GPIO.output( pin_number, GPIO.LOW )
        print('Amp on.')

    elif switch == 'off' :
        GPIO.output( pin_number, GPIO.HIGH )
        print('Amp off.')

    elif switch == 'state' :
        return GPIO.input( pin_number )

    else :
        print('"on", "off" or "state".')

##########################
#
# command line
#
##############################

if __name__ == '__main__' :

    output = ampli_control( sys.argv[1] )

    if not output is None :
        print(output)
