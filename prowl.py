from bs4 import BeautifulSoup
import urllib2
import sys
from itertools import izip
import string
import argparse
import requests

GOOGLE = []

parser = argparse.ArgumentParser(description="Scrape LinkedIn for staff members")
parser.add_argument("-u", "--url", help="URL of a public profile to start a basic search from")
parser.add_argument("-c", "--company", help="Company to search for")
args = parser.parse_args()

URLS = []

##########################

def greppage(org, link):
	#Setting User Agent#######
	header = {'User-Agent': 'WatchFish'} #Needed to prevent 403 error on Wikipedia
	##########################
	#Making HTTP req##########
	req = requests.get(link,headers=header)
	page = req.text
	soup = BeautifulSoup(page, "lxml")
	for td in soup.findAll("li", { "class":"profile-card" }):
		item = td.getText()
		print td.find('a')['href']
		URLS.append(td.find('a')['href'].lower())	 	
		try:
			for i in URLS:
				#Setting User Agent#######
				header = {'User-Agent': 'WatchFish'} #Needed to prevent 403 error on Wikipedia
				##########################
				#Making HTTP req##########
				req = urllib2.Request(i,headers=header)
				page = urllib2.urlopen(req)
				soup = BeautifulSoup(page, "lxml")
				for td in soup.findAll("li", { "class":"profile-card" }):
					url = td.find('a')['href'].lower()
					profile = td.getText().lower()
					if org.lower() in profile:
				     	 if url not in URLS:
				    	 	URLS.append(url)
				    	 	print profile + "          from           " + i    	 	
				    	 	
		except:
			pass
	print "\n".join(URLS)

def deep_and_thorough(org):	
  global GOOGLE, EMAILS, URLS
  company2 = org.lower()
  company3 = company2.replace(" ", "+")
  #Setting User Agent#######
  header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
  ##########################
        
  #Making HTTP req##########
  print "Searching Yahoo..."
  req = urllib2.Request("https://uk.search.yahoo.com/search?p="+company3+"%20linkedin%20/pub/")
  page = urllib2.urlopen(req)
  soup = BeautifulSoup(page, "lxml")
  ##########################

  company = soup.findAll("h3", {"class" : "title"})

  for i in company:
    c = i.find("a")
    print c
    GOOGLE.append(c['href'])

  ##########################

  print "---------------------------------------"
  print "Searching for " + org
  print "----------------------------------------"

  for link in GOOGLE:
    try:
      if "linkedin.com/pub/" or "linkedin.com/in/" in link:
        #print link
        URLS.append(link)
      else:
        print "non-company link"
    except: "Yahoo dun goofed"  

  for i in URLS:
  	try:
		#Setting User Agent#######
		header = {'User-Agent': 'WatchFish'} #Needed to prevent 403 error on Wikipedia
		##########################
		#Making HTTP req##########
		req = urllib2.Request(i,headers=header)
		page = urllib2.urlopen(req)
		soup = BeautifulSoup(page, "lxml")
		for td in soup.findAll("li", { "class":"profile-card" }):
			url = td.find('a')['href']
			profile = td.getText().lower()
			if company3 in profile:
		     	 if url not in URLS:
		    	 	URLS.append(url)
		    	 	print profile + "       " + url
	except:
		pass   

if args.url:
    greppage(args.company,args.url)
else:
    deep_and_thorough(args.company)
