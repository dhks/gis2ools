#!/usr/bin/env python

# Copyright (C) 2014 DhakaHackerSpace
#
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
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import ConfigParser


def main():
    print "Gis2ools uses OAuth tokens. If you don't have a personal token," \
          "create one from here https://github.com/settings/applications"
    token = raw_input("Provide your personal access token: ")
    config = ConfigParser.RawConfigParser()
    config.add_section('Credentials')
    if not token:
        token = None
    config.set('Credentials', 'Token', token)
    filename = os.path.join(os.path.expanduser('~'), '.gis2ools/gis2ools.ini')
    if not os.path.exists(os.path.dirname(filename)):
        os.makedirs(os.path.dirname(filename))
    with open(filename, 'wb') as config_file:
        config.write(config_file)
    print "\nDone!"

if __name__ == '__main__':
    main()