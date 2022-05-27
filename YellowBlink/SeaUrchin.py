import sys
sys.path.append('../YellowBlink/YellowBlink')
from gpiozero import LED, Button, RotaryEncoder
from signal import pause
from RotaryPlayer import Players

#####################
#
# GPIO 
#
######################

led = LED(17)
switch_button = Button(23, bounce_time = 0.01)
play_button = Button(11, bounce_time = 0.01)
knob = RotaryEncoder(9, 10)

#######################
#
# Actions
#
######################

knob.when_rotated_clockwise = Players.next
knob.when_rotated_counter_clockwise = Players.previous
play_button.when_pressed = Players.play_or_stop
switch_button.when_pressed = Players.next_player

#knob.when_rotated_clockwise = lambda : print('next!')
#knob.when_rotated_counter_clockwise = lambda : print('previous!')
#play_button.when_pressed = lambda : print('play or stop!')
#switch_button.when_pressed = lambda : print('next player!')

pause()
