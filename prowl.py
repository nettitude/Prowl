import urllib2
import os
import git

response = urllib2.urlopen('https://raw.githubusercontent.com/Pickfordmatt/Prowl/master/Version.txt')
html = response.read()
openfile = open('Version.txt', 'r')
cversion = openfile.readline()

def welcome():
        print "#"*50
        print "Prowl"+" "*34+"Version:1.1"
        print "Author: @MattSPickford\n"
       
        
welcome()
                


if (html != cversion):
        print ""
        print ""
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
