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
import json
import subprocess
import ConfigParser
from prettytable import PrettyTable


class Handler(object):
    def __init__(self):
        self.url = 'https://api.github.com/'
        config = self.get_config()
        self.token = config.get('Credentials', 'token')

    def get_config(self):
        config = ConfigParser.ConfigParser()
        config.read(os.path.join(os.path.expanduser('~'), '.gis2ools/gis2ools.ini'))
        return config

    def create_request(self, url, token):
        command = ["curl", '-K', '-', url]
        config = ['--header "Authorization: token ' + token + '"',
                  '--header "Accept: application/json"',
                  '--header "Content-Type: application/json"',
                  "--silent"]

        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        response, _ = process.communicate(bytes('\n'.join(config).encode('utf8')))
        return json.loads(response.decode('utf8', 'ignore'))

    def create_post_request(self,json_str, url, token):
	command = ["curl",'-X','POST','-d',json_str, '-K', '-', url]
        config = ['--header "Authorization: token ' + token + '"',
                  '--header "Accept: application/json"',
                  '--header "Content-Type: application/json"',
                  "--silent"]

        process = subprocess.Popen(command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        response, _ = process.communicate(bytes('\n'.join(config).encode('utf8')))
        return json.loads(response.decode('utf8', 'ignore'))

    def get_user(self, user):
        """
        Gets user info of a gist user.
        :param user:
        :return:
        """
        print "getting user.."
        if user:
            response = self.create_request(self.url + 'users/' + user, self.token)
        else:
            response = self.create_request(self.url + 'user', self.token)
        GistPrinter.print_user(response)

    def list_gists(self, user):
        """
        Gets public and private gists of specified user when OAuth token is provided, gets only public gists otherwise.
        :param user: username whose gists are requested.
        :return: True on success.
        """
        #TODO add pagination mechanism if user has more than 30 gists
        if user:
            response = self.create_request(self.url + 'users/' + user + '/gists', self.token)
        else:
            response = self.create_request(self.url + 'gists', self.token)
        GistPrinter.print_gist(response)
        print len(response)

    def create_gist(self, file_name,gist_description):
        """
        Creates gist using OAuth token.
        :param gist_name: name of the gist.
        :return: True on success.
        """
	try:
		print "reading file..."
		content =open(file_name)
		json_req={
			  "description": ""+gist_description,
			  "public": True,
			  "files": {
			    ""+file_name: {
			      "content": ""+content.read()
			    }
			  }
			}
		print "creating gist..."
		
		response =self.create_post_request(json.dumps(json_req),self.url+ 'gists', self.token)
		print "[Done] Requested gist is created at: "+response["created_at"]
		

	except IOError:
		print "No such file"

    def delete_gist(self, gist_name):
        """
        Deletes gist using OAuth token.
        :param gist_name: name of the gist.
        :return: True on success.
        """

    def update_gist(self, gist_name):
        """
        Updates gist using OAuth token.
        :param gist_name: name of the gist.
        :return: True on success.
        """

    def handle(self, args):
        if args.command == 'info':
            self.get_user(args.user)
        elif args.command == 'list':
            self.list_gists(args.user)
	elif args.command == 'create':
	    self.create_gist(args.f,args.d)


class GistPrinter():

    @staticmethod
    def print_gist(gists):
        #TODO prettytable is not working great so far due to screen size limitations,
        #TODO need to re-write functionality for printing gists properly.
        table = PrettyTable(['Gist Name', 'Description', 'URL'])
        table.header = False
        # table.border = False
        for gist in gists:
            table.add_row([gist['files'].keys()[0], gist['description'], gist['url']])
        table.align['Gist Name'] = 'l'
        table.align['Description'] = 'l'
        table.align['URL'] = 'l'
        print table

    @staticmethod
    def print_user(user):
        print "Name: " + user['name']
        print "Email: " + user['email']
        print "Public Gists: " + str(user['public_gists'])
        print "Private Gists: " + str(user['private_gists'])
