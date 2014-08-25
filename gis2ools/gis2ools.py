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

import sys
import difflib
import argparse
from handler import Handler


def main():

    ops = ['list', 'info', 'create', 'get', 'update', 'create','delete']

    def msg(name=None):
        return 'help message'
    parser = argparse.ArgumentParser(usage=msg())
    parser.add_argument('command', type=str, help='lots of help')

    parser.add_argument('-f', '--file-name', type=str, help='gist file name', default=None)
    parser.add_argument('-d', '--description', type=str, help='description of the gist', default="")

    parser.add_argument('-u', '--user', help='user help', default=None)
    parser.add_argument('-i', '--id', type=str, help='gist id', default=None)



    args = parser.parse_args()

    try:
        args.command = args.command.lower()
        ops.index(args.command)
    except:
        didyoumean = difflib.get_close_matches(args.command, ops, 1)
        if didyoumean:
            print 'Did you mean: ' + didyoumean.pop() + '?'
        sys.exit()
    h = Handler()
    print args
    h.handle(args)

if __name__ == '__main__':
    main()
