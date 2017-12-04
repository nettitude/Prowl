#!/usr/bin/env python

import os
import git
import argparse
import requests

parser = argparse.ArgumentParser(description="Scrape LinkedIn for company staff members")
parser.add_argument("-c", "--company", help="Company to search for")
parser.add_argument("-e", "--emailformat", help='Format of house email address style. Use: <fn>,<ln>,<fi>,<li> as placeholders for first/last name/initial. e.g "<fi><ln>@company.com"')
parser.add_argument("-j", "--jobs",  help="Include available jobs in result", action='store_true')
parser.add_argument("-s", "--subdomains",  help="Find subdomains", action='store_true')
parser.add_argument("-a", "--all",  help="FIND EVERYTHING", action='store_true')
parser.add_argument("-d", "--depth", help="How many pages of Yahoo to search through", default='10')
parser.add_argument("-p", "--proxy", help="http(s)://localhost:8080", default='')
args = parser.parse_args()

def welcome():
        print "_"*50
        print ''' \n    
  _____     ______    ______  ___  ___  ___ ___
 /      \  /      \  /      \ |  \ |  \ |  \| $$
|  $$$$$$\|  $$$$$$\|  $$$$$$\| $$ | $$ | $$| $$
| $$  | $$| $$   \$$| $$  | $$| $$ | $$ | $$| $$
| $$__/ $$| $$      | $$__/ $$| $$_/ $$_/ $$| $$
| $$    $$| $$       \$$    $$ \$$   $$   $$| $$
| $$$$$$$  \$$        \$$$$$$   \$$$$$\$$$$  \$$
| $$
| $$
 \$$    \n         '''
        print "Author: @MattSPickford"
        print "_"*50
        print ""
welcome()

response = requests.get('https://raw.githubusercontent.com/pickfordmatt/Prowl/master/Version.txt')
html = response.text
openfile = open('Version.txt', 'r')
cversion = openfile.readline()

if (html != cversion):
        Join = raw_input('New version found, would you like to update? (Y/N)').lower()
        if Join == 'y':
                print "Pr0wl is not up to date, updating..."
                os.system("git fetch --all")
                os.system("git reset --hard origin/master")
                g = git.cmd.Git("https://github.com/pickfordmatt/Prowl")
        if Join == 'n':
                pass
        print ""
        print ""

import file
