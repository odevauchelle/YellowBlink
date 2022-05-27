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
# Generic player class
#
##########################

class RotaryPlayer :

    def __init__( self, streams, **commands ) :

        self.streams = streams
        self.commands = commands
        self.current_stream_index = 0
        self.current_stream = None
        self.number_of_streams = len( self.streams )

    def play( self ) :

        self.current_stream = self.commands['play']( self.streams[ self.current_stream_index ] )

    def stop( self ) :

        self.current_stream.kill() # current_stream is a subprocess object
        self.current_stream = None

    def next( self ) :

        if self.current_stream_index < self.number_of_streams - 1 :
            self.current_stream_index += 1

    def previous( self ) :

        if self.current_stream_index > 0 :
            self.current_stream_index -= 1

    def get_current_stream_name( self ) :
        return self.streams[ self.current_stream_index ]['name']

##########################
#
# Specific players
#
##########################

WebPlayer = RotaryPlayer(
    streams = webradios,
    play = lambda webradio: subprocess.Popen( [ 'mplayer', webradio['url'] ] ),
)

DABPlayer = RotaryPlayer(
    streams = DABradios,
    play = lambda DABradio: subprocess.Popen( [ 'welle-cli', '-c', DABradio['channel'], '-p', DABradio['program'] ] ),
)

##########################
#
# Try it out
#
##########################

if __name__ == '__main__' :

    from time import sleep

    Player = WebPlayer

    for i in range(3) :
        print('\n' + Player.get_current_stream_name() + '\n')
        Player.play()
        sleep(10)
        Player.stop()
        Player.next()
