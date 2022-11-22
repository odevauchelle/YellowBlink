from subprocess import check_call, Popen
from time import sleep

########################
#
# Parameters
#
########################

player = 'mpg321'
recovery_stream = '/home/olivier/git/YellowBlink/YellowBlink/recovery_stream/Turdus_merula.mp3'

########################
#
# Mixer and volume
#
########################

#########################
#
# player
#
########################

def play( url, duration = None, volume = None ) :

    if not volume is None :
        volume_control( int( volume ) )

    try :
        play_process = check_call( [ player, url ] )
    except :
        play_process = Popen( [ player, recovery_stream ] )

    if not duration is None :
        sleep(duration)
        play_process.kill()

    return play_process


if __name__ == '__main__' :
    
    url = 'http://icecast.radiofrance.fr/fip-lofi.mp3'

    play_process = play( 'toto', duration = None )
