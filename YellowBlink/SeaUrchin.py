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
# switch_button = Button( 23, hold_time = 2 )
button = Button( 10 )
knob = RotaryEncoder( 11, 9, bounce_time = .1 )

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
# Swhich player or Shutdown
#
######################

fast_blink_kwargs = dict( on_time=.1, off_time=.1 )
slow_blink_kwargs = dict( on_time=.2, off_time=.2 )

def switch_player_or_shutdown() :

    blink()
    sleep(.5)

    if not button.is_pressed :
        Players.play_or_stop()

    else :

        blink()
        sleep(1)

        if not button.is_pressed :
            led.blink( **fast_blink_kwargs )
            Players.next_player()
            sleep(.5)
            led.on()

        else :
            led.blink( **slow_blink_kwargs )
            shutdown()


#######################
#
# Actions
#
######################

led.on()

button.when_pressed = switch_player_or_shutdown

knob.when_rotated_clockwise = ledify( Players.next )
knob.when_rotated_counter_clockwise = ledify( Players.previous )


pause()
