
#!/bin/python3
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
# Olivier Devauchelle, 2022

import os
import sys

path = os.getcwd() # current directory

from crontab import CronTab
cron = CronTab( user = True )


sleeping_beast =  sys.argv[-1]

if sleeping_beast == 'LungFish' :
    launch_progs = ['LungFish.py', 'button.py']
    cron_comments = ['YellowBlink', 'YellowBlinkInstall']
    sleep_before_launch = 30

elif sleeping_beast == 'SeaUrchin' :
    launch_progs = ['SeaUrchin.py']
    cron_comments = ['SeaUrchinInstall']
    sleep_before_launch = 15

###############
#
# Uninstall
#
###############

for comment in cron_comments :
    cron.remove_all( comment = comment )

###############
#
# Install
#
###############

if not sys.argv[1] in [ '-u', '--unistall' ] :

    for launch_prog in launch_progs :
        command = 'sleep ' + str(sleep_before_launch) + ' && (cd ' + path + '; ' + 'python3 ' + launch_prog + ')'

        job = cron.new( comment = cron_comments[-1], command = command )
        job.every_reboot()

        # welle-cli wouldn't launch with cron

        for var in ['PATH', 'SHELL'] :
            job.env[var] = os.getenv(var)

        for var in ['XDG_RUNTIME_DIR'] :
            job.env['export "' + var + '"'] = os.getenv(var)

##############
#
# check & apply
#
###############

cron.write()

for job in cron.find_comment(cron_comments[-1]) :
    print(job)
