#!/bin/python3
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
# Olivier Devauchelle, 2022

import sys
sys.path.append('../YellowBlink/YellowBlink')
from gpiozero import LED, Button, RotaryEncoder
from signal import pause
from RotaryPlayer import Players, shutdown
from time import sleep

#####################
#
# GPIO
#
######################

led = LED(17)
switch_button = Button(23, bounce_time = 0.01, hold_time = 2 )
play_button = Button(11, bounce_time = 0.01)
knob = RotaryEncoder( 10, 9 )

def blink( n = 1, blink_time = 0.1 ):

    for _ in range(n):
        led.toggle()
        sleep(blink_time)

    led.toggle()


def ledify( the_function, n = 1 ) :

    def ledified_function() :

        blink( n = n )

        the_function()

    return ledified_function

#######################
#
# Actions
#
######################

led.on()

knob.when_rotated_clockwise = ledify( Players.next )
knob.when_rotated_counter_clockwise = ledify( Players.previous )
play_button.when_pressed = ledify( Players.play_or_stop )
play_button.when_held = ledify( Players.next_player, n = 2 )
# switch_button.when_held = ledify( shutdown, n = 3 )


#knob.when_rotated_clockwise = lambda : print('next!')
#knob.when_rotated_counter_clockwise = lambda : print('previous!')
#play_button.when_pressed = lambda : print('play or stop!')
#switch_button.when_pressed = lambda : print('next player!')

pause()
