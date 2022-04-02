
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
from RadioPlayer import play_command

default_alarm_duration = 15 # minutes

def delete_alarm( alarm_index, cron ) :

    cron.remove( list( get_alarm_jobs_from_cron( cron ) )[alarm_index] )
    cron.write()

def create_alarm_job( alarm, cron ) :

    url = webradios[ alarm['webradio_name'] ][ 'url' ]

    if alarm['duration'] is None :
        alarm['duration'] = default_alarm_duration

    if len( alarm['days_of_week'] ) != 0 :

        job = cron.new( comment = 'YellowBlink', command = play_command( url, alarm['duration'], alarm['volume'] ) )
        print('>>>>', alarm['days_of_week'])
        job.dow.on(*alarm['days_of_week'])
        job.hour.on(alarm['hour'])
        job.minute.on(alarm['minute'])

    else :
        job = None

    return job

def get_alarm_jobs_from_cron( cron ) :
    return cron.find_comment('YellowBlink')

def get_alarm_from_job( job ) :

    command = job.command.split()
    command = command[ command.index('play') + 1: ]

    url = command[0]
    duration = int( command[1] )
    volume = int( command[2] )

    for name, features in webradios.items() :
        if features['url'] == url :
            break

    alarm = dict(
        days_of_week = [ int(day) for day in job.dow ],
        hour = int( str( job.hour ) ),
        minute = int( str( job.minute ) ),
        duration = duration, # seconds
        webradio_name = name,
        volume = volume
        )

    return alarm


def get_alarms_from_cron( cron ) :

    alarms = []

    for job in get_alarm_jobs_from_cron( cron ) :

        alarms += [get_alarm_from_job(job)]

    return alarms

###################################
#
# Try it out
#
###################################



if __name__ == '__main__' :

    # alarm = dict(
    #     days_of_week = [1],
    #     hour = 11,
    #     minute = 49,
    #     duration = 10, # seconds
    #     webradio_name = 'bbc4'
    #     )

    # print( alarm_to_html(alarm) )
    #

    from crontab import CronTab
    #
    cron = CronTab( user = True )
    cron.remove_all( comment = 'YellowBlink')

    # job = create_alarm_job( alarm, cron )

    # #
    # add_alarm_to_cron( alarm, cron )
    #
    # print( get_alarms_from_cron())
    #
    #

    # cron.write()
    #
    #
    print(get_alarms_from_cron(cron))

    #
    # sleep(1)
