import urllib2
import os
import git

response = urllib2.urlopen('https://raw.githubusercontent.com/Pickfordmatt/Prowl/master/Version.txt')
html = response.read()
openfile = open('Version.txt', 'r')
cversion = openfile.readline()

print html
print cversion

if (html == cversion):
        print "Pr0wl is upto date"

if (html != cversion):
        print "*" * 60
        print ""
        print ""
        print "Pr0wl is not up to date, updating..."
        os.system("git fetch --all")
        os.system("git reset --hard origin/master")
        g = git.cmd.Git("https://github.com/Pickfordmatt/Prowl")
        print ""
        print ""
        print "*" * 60


import run
