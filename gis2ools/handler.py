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


import pycurl
import StringIO

import os
import sys
import json
import time
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
        config = ['Authorization: token ' + token,
                  'Accept: application/json',
                  'Content-Type: application/json']
	
	buf = StringIO.StringIO()

	c = pycurl.Curl()
	c.setopt(pycurl.URL, url)
	c.setopt(pycurl.HTTPHEADER, config)	
	c.setopt(c.WRITEFUNCTION, buf.write)
	#c.setopt(c.POSTFIELDS, '')
	c.perform()

	json_ = buf.getvalue()
	
        return json.loads(json_.decode('utf8', 'ignore'))

    def create_post_request(self, json_str, url, token):
        config = ['Authorization: token ' + token,
                  'Accept: application/json',
                  'Content-Type: application/json']
	
	buf = StringIO.StringIO()

	c = pycurl.Curl()
	c.setopt(pycurl.URL, url)
	c.setopt(pycurl.HTTPHEADER, config)	
	c.setopt(c.WRITEFUNCTION, buf.write)
	#c.setopt(c.POSTFIELDS, '')
	c.setopt(pycurl.POST, 1)
	c.setopt(pycurl.POSTFIELDS,json_str)
	c.perform()

	json_ = buf.getvalue()
	
        return json.loads(json_.decode('utf8', 'ignore'))
	
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
            print user
            response = self.create_request(self.url + 'gists', self.token)
        GistPrinter.print_gist(response)
        print len(response)
        return response


    def create_gist(self, file_name, description):
        """
        Creates gist using OAuth token.
        :param gist_name: name of the gist.
        :return: True on success.
        """
        try:
            print "reading file..."
            content = open(file_name)
            json_req = {
                "description": "" + description,
                "public": True,
                "files": {
                    "" + file_name: {
                        "content": "" + content.read()
                        }
                }
            }
            print "creating gist..."
            response = self.create_post_request(json.dumps(json_req), self.url + 'gists', self.token)
            #print response
            print "[Done] Requested gist is created at: " + response["created_at"]
        except IOError:
            print "No such file"

    def delete_gist(self, gist_id):
        """
        Deletes gist using OAuth token.
        :param gist_name: name of the gist.
        :return: True on success.
        """
        config = ['Authorization: token ' + self.token,
                  'Accept: application/json',
                  'Content-Type: application/json']
	url=self.url + 'gists/'+gist_id;	

	buf = StringIO.StringIO()

	c = pycurl.Curl()
	c.setopt(pycurl.URL, url)
	c.setopt(pycurl.HTTPHEADER, config)	
	c.setopt(c.WRITEFUNCTION, buf.write)
	#c.setopt(c.POSTFIELDS, '')
	c.setopt(pycurl.CUSTOMREQUEST, "DELETE")
	c.perform()

	json_ = buf.getvalue()
	if len(json_)<1:
            print gist_id+" is deleted sucessfully."
	
	
#        return json.loads(json_.decode('utf8', 'ignore'))

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
            self.create_gist(args.file_name, args.description)
        elif args.command == 'delete':
            if args.id:
                self.delete_gist(args.id)
            else:
                list_gists=self.list_gists(args.user)
                n= input("Type S/N of the gist you want to delete (Hint: first cilumn of above table):")
                if n<len(list_gists):
                    self.delete_gist(self.list_gists(args.user)[int(n)-1]['id'])
                else:
                    print "Does not exist"
class GistPrinter():

    @staticmethod
    def print_gist(gists):
        #TODO prettytable is not working great so far due to screen size limitations,
        #TODO need to re-write functionality for printing gists properly.
        table = PrettyTable(['sn','id','Gist Name', 'Description', 'URL'])
        table.header = True
        table.border = True
        sn=1
        for gist in gists:
            table.add_row([sn,gist['id'],gist['files'].keys()[0], gist['description'], gist['url']])
            sn=sn+1
        table.align['id'] = 'l'
        table.align['Gist Name'] = 'l'
        table.align['Description'] = 'l'
        table.align['URL'] = 'l'
        print table

    @staticmethod
    def print_user(user):
        print "Name: " + user['name']
        print "Email: " + user['email']
        print "Public Gists: " + str(user['public_gists'])
        try:
            print "Private Gists: " + str(user['private_gists'])
        except KeyError:
            pass
