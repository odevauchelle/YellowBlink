
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

import subprocess
# import os
# import signal
import requests


##########################
#
# constants
#
##########################

webradios = [
    dict( name = 'BBC 4', url = 'http://stream.live.vc.bbcmedia.co.uk/bbc_radio_fourfm'),
    dict( name = 'NPR', url = 'https://npr-ice.streamguys1.com/live.mp3'),
    dict( name = 'FIP', url = 'http://icecast.radiofrance.fr/fip-midfi.mp3' ),
    dict( name = 'Fr. Culture', url = 'http://icecast.radiofrance.fr/franceculture-midfi.mp3'),
]

DAB = dict( channel = '8C', port = '8888' )

DABradios = [
    dict( name = 'FIP', channel = '8C', program = 'FIP', sid = '0xf204'),
    dict( name = 'France Culture', channel = '8C', program = 'FRANCE CULTURE', sid = '0xf202'),
    dict( name = 'France Info', channel = '8C', program = 'FRANCE INFO', sid = '0xf206'),
]

##########################
#
# Generic player classes
#
##########################

class RotaryPlayer :

    def __init__( self, name, streams, **commands ) :

        self.name = name
        self.streams = streams
        self.commands = commands

        self.current_stream_index = 0
        self.max_stream_index = len( self.streams ) - 1

        self.current_stream = None
        self.background_process = None

    def wake_up( self ) :

        try :
            self.background_process = self.commands['launch_background_process']()
        except :
            pass

    def sleep( self ) :

        self.stop()

        try :
            self.background_process.kill()

        except :
            print("Can't stop background_process. Using killall")
            subprocess.Popen( [ 'killall', 'welle-cli'] )

    def play( self ) :

        if self.is_playing() :
            print('Already playing')

        else :
            self.current_stream = self.commands['play']( self.streams[ self.current_stream_index ] )

    def stop( self ) :

        try :
            self.current_stream.kill() # current_stream is a subprocess object
            # os.killpg( os.getpgid( self.current_stream.pid ), signal.SIGTERM )
        except :
            print("Can't stop player. Maybe stopped already.")

        self.current_stream = None

    def switch_to( self, index ) :

        if index > self.max_stream_index :
            index = self.max_stram_index

        elif index < 0 :
            index = 0

        was_playing = self.is_playing()
        self.stop()
        self.current_stream_index = index

        if was_playing :
            self.play()

    def next( self ) :

        self.switch_to( self.current_stream_index + 1 )

    def previous( self ) :

        self.switch_to( self.current_stream_index - 1 )

    def get_current_stream_name( self ) :
        return self.streams[ self.current_stream_index ]['name']

    def get_player_name(self):
        return self.name

    def is_playing( self ) :

        if self.current_stream is None :
            return False
        else :
            return True

    def play_or_stop( self ) :

        if self.is_playing() :
            self.stop()
        else :
            self.play()


class MetaPlayer :

    def __init__( self, players ) :

        self.players = players
        self.current_index = 0
        self.max_index = len( players ) - 1

        self.get_current_player().wake_up()

    def get_current_player( self ) :
        return self.players[ self.current_index ]

    def next_player( self ) :

        was_playing = self.get_current_player().is_playing()
        self.get_current_player().sleep()

        if self.current_index < self.max_index :
            self.current_index += 1
        else :
            self.current_index = 0

        self.get_current_player().wake_up()

        if was_playing :
            self.get_current_player().play()

    def next(self) :
        self.get_current_player().next()

    def previous(self) :
        self.get_current_player().previous()

    def play(self) :
        self.get_current_player().play()

    def stop(self) :
        self.get_current_player().stop()

    def play_or_stop(self) :
        self.get_current_player().play_or_stop()

    def get_current_stream_name(self) :
        return self.get_current_player().get_player_name(), self.get_current_player().get_current_stream_name()

##########################
#
# Specific players
#
##########################

WebPlayer = RotaryPlayer(
    name = 'Web',
    streams = webradios,
    play = lambda webradio: subprocess.Popen( [ 'mplayer', webradio['url'] ] ),
)

# def launch_welle_server( channel, port ) :
#     welle_server_process = subprocess.Popen( [ 'welle-cli', '-c', channel, '-w', port ] ) # stdout = subprocess.DEVNULL, stderr = subprocess.DEVNULL )
#     # welle_server_process = subprocess.Popen( [ 'exec', 'welle-cli', '-c', channel, '-w', port ] , stdout=subprocess.PIPE, shell=True) # from Bryant Hansen, https://stackoverflow.com/questions/4789837/how-to-terminate-a-python-subprocess-launched-with-shell-true
#     current_channel = req.get("http://localhost:"  + port + "/channel") # wait until server is set up
#     return welle_server_process
#
# DABPlayer = RotaryPlayer(
#     name = 'DAB',
#     streams = DABradios,
#     launch_background_process = lambda : launch_welle_server( **DAB ),
#     play = lambda DABradio: subprocess.Popen( [ 'mplayer', 'http://localhost:' + DAB['port'] + '/mp3/' + DABradio['sid'] ] ),
# )

DABPlayer = RotaryPlayer(
    name = 'DAB',
    streams = DABradios,
    play = lambda DABradio: subprocess.Popen( [ 'welle-cli', '-T', '-c', DABradio['channel'], '-p', DABradio['program'] ] ),
)

Players = MetaPlayer( [ DABPlayer, WebPlayer ] )


##########################
#
# Other functions
#
##########################

def shutdown() :
    subprocess.call( ['sudo', 'shutdown', '-h', 'now'] )

##########################
#
# Try it out
#
##########################

if __name__ == '__main__' :

    from time import sleep

    Players.next_player()

    for i in range(3) :
        print(*Players.get_current_stream_name())
        Players.play_or_stop()
        sleep(10)
        Players.play_or_stop()
        Players.next()
