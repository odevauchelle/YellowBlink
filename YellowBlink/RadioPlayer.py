from subprocess import check_call, Popen
from time import sleep
import alsaaudio
from sys import argv as sys_argv
from os import getcwd as os_getcwd
from glob import glob

########################
#
# Parameters
#
########################

player = 'mpg123'

recovery_stream_path = '/recovery_stream/'

path = os_getcwd() # current directory
print('Current directory:', path)

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


def get_current_volume() :
    return int( mixer.getvolume()[0] )


def volume_control( value, percent_step = 5 ) :

    if value == '+' :
        value = min( [ get_current_volume() + percent_step, 100 ] )

    elif value == '-' :
        value = max( [ get_current_volume() - percent_step, 0 ] )

    mixer.setvolume( value )

    return get_current_volume()

#########################
#
# player
#
########################

def play_radio( url, duration = None, volume = None, timeout = 3 ) :

    switch_off_radio()

    if not volume is None :
        try :
            volume_control( int( volume ) )
        except :
            print('Cannot set volume.')

    ampli_control('on')

    player_process = Popen( [ player, url ] )

    if not timeout is None :

        timeout = int(timeout)

        sleep( timeout )

        if not player_process.poll() is None : # player is probably not working
            print('Failed to play stream from', url)
            print( path + recovery_stream_path + '*.mp3' )
            recovery_stream = glob( path + recovery_stream_path + '*.mp3' )[0]
            player_process = Popen( [ player, '--loop', '-1', recovery_stream ] )
            delay = 0

        else :
            delay = timeout # player is working, but we've waited already

    if not duration is None :
        sleep( int( duration ) - delay  )
        print('Duration exceeded, stopping radio.')
        switch_off_radio()

########################
#
# other functions
#
########################

def switch_off_radio() :

    try :
        check_call( [ 'killall', player ] )
    except :
        print("Can't switch off anything.")

    ampli_control('off')

def play_command( url, duration = None, volume = None ) :

    '''
    To be used in crontab.
    '''
    #(cd ./Images/; python test.py)

    command = '(cd ' + path + '; '
    command += 'python3 RadioPlayer.py play ' + url

    for kw in [duration, volume] :
        if not kw is None :
            command += ' ' + str( kw )

    command += ')'

    return command

########################
#
# command line use
#
########################

if __name__ == '__main__' :

    # For command line use

    arguments = sys_argv[1:]

    if arguments[0] == 'play' :
        play_radio( *arguments[1:] )
