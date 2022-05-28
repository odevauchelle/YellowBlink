import sys
sys.path.append('../YellowBlink/YellowBlink')
from gpiozero import LED, Button, RotaryEncoder
from signal import pause
from RotaryPlayer import Players, shutdown

#####################
#
# GPIO
#
######################

led = LED(17)
switch_button = Button(23, bounce_time = 0.01, hold_time = 2 )
play_button = Button(11, bounce_time = 0.01)
knob = RotaryEncoder( 10, 9 )

def ledify( some_function, n = 1 ) :
    def ledified_function() :
        led.blink( on_time=.1, off_time=.1, n = n, background = True )
        some_function()
        led.on()
    return ledified_function

#######################
#
# Actions
#
######################

led.on()

knob.when_rotated_clockwise = ledify( Players.next )
knob.when_rotated_counter_clockwise = ledify( Players.previous )
play_button.when_pressed = ledify( Players.play_or_stop )
switch_button.when_pressed = ledify( Players.next_player )
switch_button.when_held = ledify( shutdown, n = 3 )


#knob.when_rotated_clockwise = lambda : print('next!')
#knob.when_rotated_counter_clockwise = lambda : print('previous!')
#play_button.when_pressed = lambda : print('play or stop!')
#switch_button.when_pressed = lambda : print('next player!')

pause()
