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
from time import sleep

######################
#
# Fake player
#
######################

if sys.argv[-1] == '--fake' :

    class FakePlayers :

        def __init__(self) :
            self.name = 'Fake'

        def next(self) :
            print('next')

        def previous(self) :
            print('previous')

        def next_player(self) :
            print('next player')

        def play_or_stop(self) :
            print('play or stop')

    Players = FakePlayers()

    def shutdown() :
        print('shutdown')

else :
    from RotaryPlayer import Players, shutdown


#####################
#
# GPIO connections
#
######################

led = LED(17)
switch_button = Button(23, hold_time = 2 )
play_button = Button(11 )
knob = RotaryEncoder( 10, 9 )

#####################
#
# LED blink
#
######################

def blink( n = 1, blink_time = 0.1 ):

    for _ in range( 2*n - 1 ):
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
# Shutdown control
#
######################

def switch_player_or_switch_off() :

    if play_button.is_held :
        blink(5)
        shutdown()

    else :
        blink(2)
        Players.next_player()

#######################
#
# Actions
#
######################

led.on()

knob.when_rotated_clockwise = ledify( Players.next )
knob.when_rotated_counter_clockwise = ledify( Players.previous )
play_button.when_released = ledify( Players.play_or_stop )

switch_button.when_held = switch_player_or_switch_off


pause()
