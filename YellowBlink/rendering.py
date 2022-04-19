
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


from webradios import webradios
from datetime import datetime
from socket import gethostname

####################
#
# Parameters
#
###################

main_color = 'DarkCyan'
faded_color = 'grey'
light_faded_color = 'LightGrey'

separator = '&nbsp; <span style="color: ' + light_faded_color + '">&bull;</span> &nbsp;'

# hrule = '<hr color=' + light_faded_color + '>\n'
hrule = '<hr style="border: 1px dashed ' + light_faded_color + ';">'

default_alarm = dict(
        days_of_week = [],
        hour = 12,
        minute = 0,
        duration = 60*5, # seconds
        webradio_name = 'fip'
        )

i_days = [ 1, 2, 3, 4, 5, 6, 0 ]
weekdays = [ 'Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat' ]

##############################
#
# html header
#
##############################

static_header = '''
<style>
a{ color:''' + main_color + '''; text-decoration: none;}
p{ text-align: center;}
body {
    background-color: white;
    max-width: 30em;
    margin: 0 auto;
}
</style>

<meta name="viewport" content="width=device-width, initial-scale=1">
<head>
  <title>LungFish</title>
  <link rel="shortcut icon" href="/static/favicon.svg" type="image/x-icon" />
</head>
'''

def get_header( with_time = True ) :

    html = static_header

    now = datetime.now()

    if with_time :
        html += '<p>'
        html += '<br>'
        html += '&#64;' + gethostname() + separator
        html += now.strftime("%H:%M" + separator + "%b %d, %Y")
        html += '</p>'

    return html

####################
#
# Functions
#
###################

def stop_bar() :

    html = '<a href="/off">Stop</a>'

    return html

def volume_control_bar( current_volume = None ) :

    html = ''

    html += '<a href="/volume/down">&#9661;</a>' + 5*'&nbsp;'
    html += 'Volume ' + str(current_volume) + 5*'&nbsp;'
    html += '<a href="/volume/up">&#9651;</a>'

    return html

def alarm_to_html( alarm, alarm_index ) :

    html = ''
    day_space = '&emsp;'

    for i in i_days :

        day = weekdays[i]

        if i in alarm['days_of_week'] :
            style = "background-color: " + light_faded_color
            # style += "; color: " + main_color
        else :
            style = "color: grey"

        html += '<span style="' + style + '">'
        html += day
        html += '</span>'
        html += day_space

    html = html[:-len(day_space)] # remove last space

    html += '<br>'

    html += str( alarm['hour'] ) + ':' + "{:02d}".format( alarm['minute'] ) + ' '
    html += separator
    html += webradios[alarm['webradio_name']]['full_name'] + ' '
    html += separator
    html += str( alarm['duration']//60 ) + ' min'
    html += separator
    html += 'Vol. ' + str( alarm['volume'] )
    html += separator
    html += '<a href="/edit/' + str(alarm_index) + '">Edit</a>'
    html += separator
    html += '<a href="/delete/' + str(alarm_index) + '">Del.</a>'

    return html

def homepage_template( alarms, webradios, current_volume = None ) :

    html = get_header()

    html += hrule

    # Radios
    html += '<p align="left">'

    for name in webradios.keys() :
        html += '<a href="/play/' + name + '">' + webradios[name]['full_name'] + '</a>'
        html += separator

    html = html[:-len(separator)]

    html += '</p>'

    # Stop

    html += '<p align="center">'
    html += stop_bar()
    html += '</p>'

    html += hrule


    # Volume
    html += '<p align="left">'
    html += volume_control_bar( current_volume )
    html += '</p>'

    html += hrule

    # Alarms
    for i, alarm in enumerate( alarms ) :
        html += '<p>' + alarm_to_html( alarm, i ) + '</p>'

    html += '<p align="left"><a href="/edit/new">New alarm</a></p>'

    return html

def edit_alarm_template( alarm = None, name = 'new', current_volume = 0 ) :

    html = get_header()

    html += hrule

    if alarm is None :
        alarm = default_alarm.copy()
        alarm['volume'] = current_volume

    html += '<form action="/edit/' + name +  '" method="post">'

    # time
    html += '<p>Time '
    html += '<input name="hour" size="2" type="number" min=0 max=23 value=' + str(alarm['hour']) + ' />:'
    html += '<input name="minute" size="2" type="number" min=0 max=59 value=' + str(alarm['minute']) + ' /></p>'

    # days
    html += '<p text-align = "left">'
    for i in i_days :

        day = weekdays[i]
        html += '<div>'
        html += '<input type="checkbox" '
        if i in alarm['days_of_week'] :
            html += 'checked '
        html += 'name="day_' + str(i) + '">'
        html += ' ' + day
        html += '</div>'
    html += '</p>'

    # webradio
    html += '<p>Webradio '
    html += '<select name = "webradio" >\n'
    for name, webradio in webradios.items() :

        if name == alarm['webradio_name'] :
            is_selected = ' selected '
        else :
            is_selected = ''

        html += '<option value="' + name + '"' + is_selected + '>' + webradio['full_name'] + '</option>\n'
    html += '</select></p>'

    # duration
    html += '<p>Duration '
    html += '<input name="duration" size="3" type="number" min=0 max=120 value=' + str( int(alarm['duration']/60) ) + ' /> min</p>'

    # volume
    html += '<p>Volume '
    html += '<input name="volume" size="3" type="number" min=0 max=100 value=' + str( int( alarm['volume'] ) ) + ' /></p>'

    html += hrule

    # submit form
    html += '<p><input value="Set alarm" type="submit" />'
    html += separator
    html +='<a href="/home">Cancel</a></p>'
    html += '</form>'

    return html
