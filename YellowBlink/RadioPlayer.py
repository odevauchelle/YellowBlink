
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
import subprocess
import alsaaudio
#importing the os module
import os

def get_mixer( sound_card_number = 0 ) :
    return alsaaudio.Mixer( control='Speaker', cardindex = sound_card_number )

#########################
#
# Mixer Settings
#
#########################

for sound_card_number in range(5) :
    try :
        mixer = get_mixer( sound_card_number )
        break

    except :
        pass

try :
    mixer
    print( 'Soundcard: ', sound_card_number )

except :
    print('No soundcard found!')

#########################
#
# Commands
#
#########################

def play_command( url, duration = None, volume = None ) :

    '''
    To be used in crontab.
    '''

    command = 'python3 '
    command += os.getcwd() # current directory
    command += '/RadioPlayer.py play ' + url

    for kw in [duration, volume] :
        if not kw is None :
            command += ' ' + str( kw )

    return command

def play_radio( url, duration = None, volume = None ) :

    if not volume is None :
        volume_control( int( volume ) )

    command = 'mplayer'

    if not duration is None :
        command += ' -endpos ' + str( duration )

    command += ' ' + url

    command += ' </dev/null >/dev/null 2>&1 &' # NO OUTPUT

    subprocess.Popen( command.split() )


def kill_command() :
    return 'killall mplayer'


def get_current_volume() :
    return int( mixer.getvolume()[0] )


def volume_control( value, percent_step = 10 ) :

    if value == '+' :
        value = min( [ get_current_volume() + percent_step, 100 ] )

    elif value == '-' :
        value = max( [ get_current_volume() - percent_step, 0 ] )

    mixer.setvolume( value )

    return get_current_volume()


def switch_off_radio() :
    subprocess.Popen( kill_command().split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE ).communicate()

if __name__ == '__main__' :

    # For command line use

    arguments = sys.argv[1:]

    if arguments[0] == 'play' :
        play_radio( *arguments[1:] )
