#!/usr/bin/env python

import urllib2
import os
import git

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


response = urllib2.urlopen('https://raw.githubusercontent.com/Pickfordmatt/Prowl/master/Version.txt')
html = response.read()
openfile = open('Version.txt', 'r')
cversion = openfile.readline()

if (html != cversion):
        Join = raw_input('New version found, would you like to update? (Y/N)').lower()
        if Join == 'y':
                print "Pr0wl is not up to date, updating..."
                os.system("git fetch --all")
                os.system("git reset --hard origin/master")
                g = git.cmd.Git("https://github.com/Pickfordmatt/Prowl")
        if Join == 'n':
                pass
        print ""
        print ""

import file
