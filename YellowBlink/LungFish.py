
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


from bottle import route, run, get, post, request, redirect
from crontab import CronTab

from webradios import webradios
from RadioPlayer import *
from alarm import *
from rendering import *

#########################
#
# Main page
#
#########################

@route('/home')
def home():
    cron = (CronTab( user = True ))
    alarms = get_alarms_from_cron( cron )
    return homepage_template( alarms, webradios, get_current_volume() )

@route('/delete/<index>')
def delete( index ) :
    delete_alarm( int( index ), CronTab( user = True ) )
    return redirect("/home")

@route('/off')
def switch_off():
    switch_off_radio()
    return redirect("/home")

@route('/play/<radio_name>')
def play( radio_name ) :
    switch_off_radio()
    play_radio( webradios[radio_name]['url'])
    return redirect("/home")

@route('/volume/<value>')
def adjust_volume( value ) :

    if value == 'up' :
        volume_control( '+' )

    elif value == 'down' :
        volume_control( '-' )

    return redirect("/home")

#########################
#
# Edit alarm
#
#########################

@get('/edit/<index>')
def edit_alarm( index ):
    if index == 'new' :
        return edit_alarm_template( name = index )
    else :
        cron = CronTab( user = True )
        alarms = get_alarms_from_cron( cron )
        return edit_alarm_template( alarm = alarms[ int(index) ], name = index )

@post('/edit/<index>')
def set_alarm( index ):

    alarm = dict(
        hour = int( request.forms.get('hour') ),
        minute = int( request.forms.get('minute') ),
        webradio_name = request.forms.get('webradio'),
        duration = int( request.forms.get('duration') )*60, # seconds
        volume = int( request.forms.get('volume') )
        )

    alarm['days_of_week'] = []

    for i in i_days :

        if not request.forms.get('day_' + str(i)) is None :
            alarm['days_of_week'] += [ i ]

    print(alarm['days_of_week'])

    cron = (CronTab( user = True ))

    if index != 'new' :
        cron.remove( list( get_alarm_jobs_from_cron( cron ) )[int(index)] )

    create_alarm_job( alarm, cron )

    cron.write()

    return redirect("/home")

#########################
#
# Deploy
#
#########################

run( host='localhost', port=8080, debug = True )
# run( host='0.0.0.0', port=8080, debug = False )
