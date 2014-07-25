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

from setuptools import setup


setup(name='gis2ools',
      version='0.1',
      description='Gist Command-line tool',
      url='http://github.com/dhks/gis2ools/',
      license='GPLv2',
      packages=['gis2ools'],
      entry_points={
          'console_scripts': [
              'gis2ools = gis2ools.gis2ools:main',
              'gis2ools-configure = gis2ools.gis2ools_configure:main',
          ],
      },
      install_requires=['prettytable'],
      zip_safe=False,
      classifiers=[
          "Development Status :: 1 - Alpha",
          "Topic :: Utilities",
          "Environment :: Console",
      ],
)