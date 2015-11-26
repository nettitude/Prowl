#Importing Libs##########
from bs4 import BeautifulSoup
import urllib2
import sys
from itertools import izip
import string
import argparse
import random

#########################

URLS = []
EMAILS = []
GOOGLE = []


parser = argparse.ArgumentParser(description="Scrape LinkedIn for staff members")
parser.add_argument("-u", "--url", help="URL of a public profile to start a basic search from")
parser.add_argument("-c", "--company", help="Company to search for")
parser.add_argument("-o", "--outfile", help="Filename to write results to")
parser.add_argument("-e", "--emailformat", help="Format of house email address style. Use: <fn>,<ln>,<fi>,<li> as placeholders for first/last name/initial. e.g <fi><ln>@company.com")
parser.add_argument("-d", "--debug", action="store_true", help="Turn on debug output")
args = parser.parse_args()

def deep_and_thorough( Org ):	
  global GOOGLE, EMAILS, URLS
  Org2 = Org.lower()

  if args.debug:
    print "deep_and_thorough( "+Org+" )"

  company2 = Org2.replace(" ", "")
  #Setting User Agent#######
  header = {'User-Agent': 'Mozilla/5.0'} 
  ##########################
        
  #Making HTTP req##########
  if args.debug:
    print "Searching Yahoo..."
  req2 = urllib2.Request("https://uk.search.yahoo.com/search?p="+company2+"%20linkedin%20")
  page2 = urllib2.urlopen(req2)
  if args.debug:
    print "Page\n\n" + str( page2 )
  soup2 = BeautifulSoup(page2, "lxml")
  ##########################

  company2 = soup2.findAll("h3", {"class" : "title"})

  if args.debug:
    print str(len(company2)) + " results found"

  for i2 in company2:
    c2 = i2.find("a")
    if args.debug:
      print c2['href']
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

def greppage(link, org ):
  global GOOGLE, EMAILS, URLS, target, args
  
  if args.debug:
    print "greppage( '"+link+"', '"+org+"')"
 
  ua1 = ['Fire', 'Ice', 'Magic', 'Slippery', 'Spectacular', 'Easy', 'Genius', 'Grumpy','Buttery','Spicey']
  ua2 = ['fox','weasel','donkey','ocelot','stoat','rabbit','wombat','tapir','squirrel','otter','hedgehog']
  useragent = random.choice(ua1) + random.choice(ua2) + " v" + str(random.randrange(0,60) + random.random())
  if args.debug:
    print "User agent: " + useragent

  #Setting User Agent#######
  header = {'User-Agent': 'Mozilla/5.0 ' + useragent}
  ##########################
  
  if args.debug:
    print "Requesting linkedin profile"
  
  #Making HTTP req##########
  req = urllib2.Request(link,headers=header)
  page = urllib2.urlopen(req)
  soup = BeautifulSoup(page, "lxml")
 
  # Check this user, use the headline and current employment from the profile page
  profile = soup.find("div", class_="profile-overview-content")
  process_person( profile.find("h1", id="name"), profile.find( "p", class_="headline" ) + " " + profile.find( "span", class_="org" ), link, org )

  cards = soup.find_all("li", class_="profile-card")
  if args.debug:
    print str(len(cards)) + " cards found"
    print cards
    print "Looping through cards"

  for card in cards:
    # if args.debug:
    #   print "Card:"
    #   print card
   
    name = card.find("h4").find("a").get_text()
    company = card.find("p", class_="headline").get_text()
    url = card.find("a")["href"]
    
    process_person( name, company, url, org )


def process_person( name, company, url, org ):
  if args.debug:
    print name
    print company
    print url
    print "Testing if "+org.lower()+" is in \"" + company.lower() + "\""
  if org.lower() in company.lower():
    if args.debug:
      print "Company identified in job title"
    if url not in URLS:
      if args.debug:
        print "New URL found, adding"
      URLS.append(url)
      data = name + chr(9) + company + chr(9) + url
      data = filter(lambda x: x in string.printable, data)
      sys.stdout.write( data )
      target.write( data + "\n" )
      if args.emailformat:
        fn = string.split(name)[0]
        fi = fn[0]
        ln = ''.join(string.split(name)[1:])
        li = ln[1]
        email = args.emailformat.replace('<fn>',fn).replace('<ln>',ln).replace('<fi>',fi).replace('<li>',li).lower()
        email2 = filter(lambda x: x in string.printable, email)
        sys.stdout.write( chr(9) + email2 )
        f = open( outfile + '.emails', 'a' )
        f.write( email2 + "\n" )
      sys.stdout.write( "\n" )

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
      f = open( outfile + '.emails', 'a' )
      f.write( email2 + "\n" )
      


  except:
    print "oops you've got an error"

if args.debug:
  print args

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
