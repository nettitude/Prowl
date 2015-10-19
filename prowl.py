#Importing Libs##########
from bs4 import BeautifulSoup
import urllib2
import sys
from itertools import izip
import string
import argparse
#########################

URLS = []
EMAILS = []
GOOGLE = []


parser = argparse.ArgumentParser(description="Scrape LinkedIn for staff members")
parser.add_argument("-u", "--url", help="URL of a public profile to start a basic search from")
parser.add_argument("-c", "--company", help="Company to search for")
parser.add_argument("-o", "--outfile", help="Filename to write results to")
parser.add_argument("-e", "--emailformat", help="Format of house email address style. Use: <fn>,<ln>,<fi>,<li> as placeholders for first/last name/initial. e.g <fi><ln>@company.com")
# parser.add_argument("-h", "--help", action="store_true", help="Show help")
args = parser.parse_args()

def deep_and_thorough( Org ):	
  global GOOGLE, EMAILS, URLS
  Org2 = Org.lower()

  company2 = Org2.replace(" ", "")
  #Setting User Agent#######
  header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
  ##########################
        
  #Making HTTP req##########
  req2 = urllib2.Request("https://uk.search.yahoo.com/search?p="+company2+"%20linkedin%20/pub/")
  page2 = urllib2.urlopen(req2)
  soup2 = BeautifulSoup(page2, "lxml")
  ##########################

  company2 = soup2.findAll("h3", {"class" : "title"})

  for i2 in company2:
    c2 = i2.find("a")
    #print c2['href']
    GOOGLE.append(c2['href'])

  ##########################

  print "---------------------------------------"
  print "Searching for " + Org
  print "----------------------------------------"

  for link in GOOGLE:
    try:
      #print link
      if "linkedin.com/pub/" or "linkedin.com/in/" in link:
        greppage(link, Org)
        for iturl in URLS:
          greppage(iturl, Org)
      else:
        print "non-company link"
    except: "Yahoo dun goofed"    

  GOOGLE = []

def basic_search( Org, link ):
  global GOOGLE, EMAILS, URLS
  Org = Org.lower()

  ##########################

  print "---------------------------------------"
  print "Searching for " + Org
  print "----------------------------------------"

  greppage(link, Org)

  for iturl in URLS:
    try:
      greppage(iturl, Org)
    except:
      print "You dun goofed"

def greppage(link, Org ):
  global GOOGLE, EMAILS, URLS, target, args
  x=1
  #Setting User Agent#######
  header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
  ##########################
  
  #Making HTTP req##########
  req = urllib2.Request(link,headers=header)
  page = urllib2.urlopen(req)
  soup = BeautifulSoup(page, "lxml")
  ##########################
  name = soup.select("div.insights-browse-map > ul > li > h4 > a")
  company = soup.select("div.insights-browse-map > ul > li > p.browse-map-title")

  while x == 1: 
    global PRINT
    PRINT = []
    list1 = []
    list2 = []
    list3 = []

    for i in name:
      list1.append(i.getText())	
      list3.append(i['href'])
      #print i.getText()
        
    for c in company: 
      list2.append(c.getText().lower() + ",")
      #print c.getText()

    for item in izip(list1, list2, list3):
      #print item
      if Org.lower() in item[1]:	
        if item[2] not in URLS:
          ##print item[0]+chr(9)+ item[1]+ chr(9) +item[2]
          URLS.append(item[2])
          EMAILS.append(item[0])
          pre=(item[0]+ chr(9) + item[1]+ chr(9) +item[2])
          data = filter(lambda x: x in string.printable, pre)
          PRINT.append(data)
          target.write(data + "\n")			
          if args.emailformat:
            fn = string.split(item[0])[0]
            fi = fn[0]
            ln = ''.join(string.split(item[0])[1:])
            li = ln[1]
            email = args.emailformat.replace('<fn>',fn).replace('<ln>',ln).replace('<fi>',fi).replace('<li>',li).lower()
            email2 = filter(lambda x: x in string.printable, email)
            ##print email2
            f = open( outfile + '.emails', 'a' )
            f.write( email2 + "\n" )
            
    x+=1

def mangle_emails(names, pattern, orgname):
  global outfile
  try:
    for name in names:
      fn = string.split(name)[0]
      fi = fn[0]
      ln = ''.join(string.split(name)[1:])
      li = ln[1]
      email = pattern.replace('<fn>',fn).replace('<ln>',ln).replace('<fi>',fi).replace('<li>',li).lower()
      email2 = filter(lambda x: x in string.printable, email)
      ##print email
      f = open( outfile + '.emails', 'a' )
      f.write( email2 + "\n" )
  except:
    print "oops you've got an error"

if args.company:
  if args.outfile:
    outfile = args.outfile
  else:
    outfile = args.company.replace(' ','_')+".output.txt"
  target = open(outfile, 'a')
  
  # Basic quick search if there's a URL provided
  if args.url:
    basic_search(args.company,args.url) 
  else:
    deep_and_thorough(args.company)

  if args.emailformat:
    mangle_emails( EMAILS, args.emailformat, args.company ) 
  sys.exit(0)
else:
  parser.print_usage()
