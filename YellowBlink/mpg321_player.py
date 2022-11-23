from subprocess import check_call, Popen
from time import sleep
import alsaaudio

########################
#
# Parameters
#
########################

player = 'mpg321'
recovery_stream = './recovery_stream/Turdus_merula.mp3'

########################
#
# Control ampli
#
########################

try :
    from ampli import ampli_control
    ampli_control('off')

except :

    def ampli_control( on_off ) :
        print('Cannot switch', on_off, 'ampli.' )


########################
#
# Mixer and volume
#
########################

def get_mixer( control = 'Speaker', cardindex = 0 ) :
    return alsaaudio.Mixer( control = control, cardindex = cardindex )

for cardindex in range(5) :

    for control in ('Speaker', 'Analogue') :

        try :
            mixer = get_mixer( control=control, cardindex = cardindex )
            break

        except :
            pass

try :
    mixer
    print( 'Soundcard: ', cardindex, 'Control:', control )

except :
    print('No soundcard found!')


#########################
#
# player
#
########################

def play( url, duration = None, volume = None, timeout = 3 ) :

    if not volume is None :
        try :
            volume_control( int( volume ) )
        except :
            print('Cannot set volume.')

    ampli_control('on')

    player_process = Popen( [ player, url ] )

    sleep( timeout )

    if not player_process.poll() is None : # player is probably not working
        player_process = Popen( [ player, recovery_stream ] )

    else :
        duration -= timeout # player is working, but we've waited already

    if not duration is None :
        sleep( duration )
        switch_off_radio()

########################
#
# other functions
#
########################

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

    Popen( [ 'killall', player ] )

    ampli_control('off')


########################
#
# command line use
#
########################

if __name__ == '__main__' :

    url = 'http://icecast.radiofrance.fr/fip-lofi.mp3'

    play_process = play( 'toto', duration = 3 )
