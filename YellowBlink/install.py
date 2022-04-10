
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

import os

path = os.getcwd() # current directory

from crontab import CronTab
cron = CronTab( user = True )

launch_progs = ['LungFish.py', 'button.py']

###############
#
# Uninstall
#
###############

for comment in ['YellowBlink', 'YellowBlinkInstall'] :
    cron.remove_all( comment = comment )

###############
#
# Install
#
###############

for launch_prog in launch_progs :
    command = '(cd ' + path + '; ' + 'python3 ' + launch_prog + ')'
    job = cron.new( comment = 'YellowBlinkInstall', command = command )
    job.every_reboot()
cron.write()

##############
#
# check
#
###############

for job in cron.find_comment('YellowBlinkInstall') :
    print(job)
