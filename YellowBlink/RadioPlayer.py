
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


import subprocess

def play_command( url, duration = None, output = True ) :

    command = 'mplayer'

    if not duration is None :
        command += ' -endpos ' + str( duration )

    command += ' ' + url

    if not output :
        command += ' </dev/null >/dev/null 2>&1 &'
    # ['mplayer', webradios[name]['url'], '</dev/null', '>/dev/null', '2>&1', '&' ]

    return command

def kill_command() :
    return 'killall mplayer'

def volume_control( value ) :
    return 'amixer -D pulse set Master ' + value

def play_radio( url ) :
    subprocess.Popen( play_command( url, output = False ).split() )

def switch_off_radio() :
    subprocess.Popen( kill_command().split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE ).communicate()
