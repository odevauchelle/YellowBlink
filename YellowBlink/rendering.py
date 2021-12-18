
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

separator = '&nbsp; | &nbsp;'

default_alarm = dict(
        days_of_week = [],
        hour = 12,
        minute = 0,
        duration = 60*5, # seconds
        webradio_name = 'fip'
        )

weekdays = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']

##############################
#
# html header
#
##############################

static_header = '''
<style>

a{ color:''' + main_color + '''; text-decoration: none;}

p{ text-align: center;}

</style>

<meta name="viewport" content="width=device-width, initial-scale=1">
'''

def get_header( with_time = True ) :
    html = static_header

    now = datetime.now()

    if with_time :
        html += '<p>'
        html += '&#64;' + gethostname() + separator
        html += now.strftime("%H:%M" + separator + "%b %d, %Y")
        html += '</p>'

    return html

####################
#
# Functions
#
###################

def volume_control_bar() :

    html = ''

    html += '<a href="/volume/down">&#8681;</a>' + separator
    html += '<a href="/off">Stop</a>' + separator
    html += '<a href="/volume/up">&#8679;</a>'

    return html

def alarm_to_html( alarm, alarm_index ) :

    html = ''

    for i, day in enumerate( weekdays ) :

        i += 1

        if i in alarm['days_of_week'] :
            style = "background-color: LightGrey"
            # style += "; color: " + main_color
        else :
            style = "color: grey"

        html += '<span style="' + style + '">'
        html += day
        html += '</span>'
        html += ' '

    html += '<br>'

    html += str( alarm['hour'] ) + ':' + "{:02d}".format( alarm['minute'] ) + ' '
    html += separator
    html += webradios[alarm['webradio_name']]['full_name'] + ' '
    html += separator
    html += str( alarm['duration']//60 ) + ' min'
    html += separator
    html += '<a href="/edit/' + str(alarm_index) + '">Edit</a>'
    html += separator
    html += '<a href="/delete/' + str(alarm_index) + '">Delete</a>'

    return html

def homepage_template( alarms, webradios ) :

    html = get_header()

    # Radios
    html += '<p align="left">'

    for name in webradios.keys() :
        html += '<a href="/play/' + name + '">' + webradios[name]['full_name'] + '</a>'
        html += separator

    html = html[:-len(separator)]

    html += '</p>'

    # Volume
    html += '<p align="left">'
    html += volume_control_bar()
    html += '</p>'

    # Alarms
    for i, alarm in enumerate( alarms ) :
        html += '<p>' + alarm_to_html( alarm, i ) + '</p>'

    html += '<p align="left"><a href="/edit/new">New alarm</a></p>'

    return html

def edit_alarm_template( alarm = None, name = 'new' ) :

    html = get_header()

    if alarm is None :
        alarm = default_alarm.copy()

    html += '<form action="/edit/' + name +  '" method="post">'

    # time
    html += '<p>Time '
    html += '<input name="hour" type="number" min=0 max=23 value=' + str(alarm['hour']) + ' />:'
    html += '<input name="minute" type="number" min=0 max=59 value=' + str(alarm['minute']) + ' /></p>'

    # days
    html += '<p text-align = "left">'
    for i, day in enumerate(weekdays) :
        i += 1
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
    html += '<select name = "webradio">\n'
    for name, webradio in webradios.items() :
        html += '<option value="' + name + '">' + webradio['full_name'] + '</option>\n'
    html += '</select></p>'

    # duration
    html += '<p>Duration '
    html += '<input name="duration" type="number" min=0 max=120 value=' + str(int(alarm['duration']/60) ) + ' /> min</p>'

    # submit form

    html += '<p><input value="Set alarm" type="submit" />'
    html += separator
    html +='<a href="/home">Cancel</a></p>'
    html += '</form>'

    return html
