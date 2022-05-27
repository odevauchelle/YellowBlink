import subprocess

##########################
#
# constants
#
##########################

webradios = [
    dict( name = 'BBC 4', url = 'http://stream.live.vc.bbcmedia.co.uk/bbc_radio_fourfm'),
    dict( name = 'NPR', url = 'https://npr-ice.streamguys1.com/live.mp3'),
    dict( name = 'FIP', url = 'http://icecast.radiofrance.fr/fip-lofi.mp3' ),
    dict( name = 'Fr. Culture', url = 'http://icecast.radiofrance.fr/franceculture-lofi.mp3'),
]

DABradios = [
    dict( name = 'FIP', channel = '8C', program = '"FIP"'),
    dict( name = 'France Culture', channel = '8C', program = '"FRANCE CULTURE"'),
    dict( name = 'France Info', channel = '8C', program = '"FRANCE INFO"'),
]

##########################
#
# Generic player classes
#
##########################

class RotaryPlayer :

    def __init__( self, streams, name, **commands ) :

        self.name = name
        self.streams = streams
        self.commands = commands
        self.current_stream_index = 0
        self.current_stream = None
        self.number_of_streams = len( self.streams )

    def play( self ) :

        if self.is_playing() :
            print('Already playing')

        else :
            self.current_stream = self.commands['play']( self.streams[ self.current_stream_index ] )

    def stop( self ) :

        try :
            self.current_stream.kill() # current_stream is a subprocess object
        except :
            print("Can't stop player. Maybe stopped already.")

        self.current_stream = None

    def next( self ) :

        if self.current_stream_index < self.number_of_streams - 1 :
            self.current_stream_index += 1

    def previous( self ) :

        if self.current_stream_index > 0 :
            self.current_stream_index -= 1

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

    def get_current_player( self ) :
        return self.players[ self.current_index ]

    def next_player( self ) :

        was_playing = self.get_current_player().is_playing()
        self.get_current_player().stop()

        if self.current_index < self.max_index :
            self.current_index += 1
        else :
            self.current_index = 0

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
    streams = webradios,
    name = 'Web',
    play = lambda webradio: subprocess.Popen( [ 'mplayer', webradio['url'] ] ),
)

DABPlayer = RotaryPlayer(
    streams = DABradios,
    name = 'DAB',
    play = lambda DABradio: subprocess.Popen( [ 'welle-cli', '-c', DABradio['channel'], '-p', DABradio['program'] ] ),
)

Players = MetaPlayer( [ DABPlayer, WebPlayer ] )

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
