gis2ools
========

Command-line Gist client


### Installation

#### On Ubuntu
    apt-get install python-setuptools
    apt-get install python-virtualenv

#### On Mac OSX
    easy_install virtualenv
    (or use brew instead)

#### Create isolated Python environment using virtualenv,
    virtualenv MyGis2ools
    cd MyGis2ools

#### Clone this repository:
    git clone https://github.com/dhks/gis2ools.git

#### Install gis2ools:
    cd gis2ools
    python setup.py install

### Configure
    gis2ools-configure

### Usage:
    gis2ools list
    gis2ools info [user]
    gis2ools create <gist_name>
    gis2ools get <gist_name>
    gis2ools update <gist_name>
    gis2ools delete <gist_name>