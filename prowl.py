
from bs4 import BeautifulSoup
import urllib2
import sys
from itertools import izip
import string
import argparse
import requests
from colorama import Fore, Back, Style
from colorama import init

GOOGLE = []

parser = argparse.ArgumentParser(description="Scrape LinkedIn for staff members")
parser.add_argument("-u", "--url", help="URL of a public profile to start a basic search from")
parser.add_argument("-c", "--company", help="Company to search for")
args = parser.parse_args()

URLS = []
FOUND = []

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
    #print td.find('a')['href']
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
          for g in td.findAll('a'):
            name = g.getText()
          else:
            pass
          for f in td.findAll('p'):
            profile = f.getText().lower()
          full = name+profile
          if org.lower() in profile.lower():
               if full not in FOUND:
                FOUND.append(full)
                print(Fore.GREEN + name + "  " + Fore.YELLOW + profile  + Style.RESET_ALL)    

    except:
      pass
def deep_and_thorough(org):	
  global GOOGLE, EMAILS, URLS
  company2 = org.lower()
  company3 = company2.replace(" ", "%20")
  #Setting User Agent#######
  header = {'User-Agent': 'Mozilla/5.0'} #Needed to prevent 403 error on Wikipedia
  ##########################
        
  #Making HTTP req##########
  print(Fore.RED + "Searching Yahoo" + Style.RESET_ALL)
  req = urllib2.Request("https://uk.search.yahoo.com/search?p="+company3+"linkedin%20profile")
  page = urllib2.urlopen(req)
  soup = BeautifulSoup(page, "lxml")
  ##########################
  company = soup.findAll("h3", {"class" : "title"})

  for i in company:
    c = i.find("a")
    GOOGLE.append(c['href'])
  ##########################
  print(Fore.GREEN + "################# FOUND ACCOUNTS #################" + Style.RESET_ALL)
  print("\n".join(GOOGLE))
  print(Fore.GREEN + "##################################################" + Style.RESET_ALL)
  print "---------------------------------------"
  print(Fore.RED + "Searching for: " + org +Style.RESET_ALL)
  print "----------------------------------------"

  for link in GOOGLE:
    try:
      if "linkedin.com/pub/" or "linkedin.com/in/" or "Linkedin.com/in/" or "Linkedin.com/in/" in link:
        #print link
        URLS.append(link)
      else:
        pass
    except: "Yahoo dun goofed"  

  for i in URLS:
  	try:
		greppage(company2, i)
	except:
		pass   
if args.url:
    greppage(args.company,args.url)
else:
    deep_and_thorough(args.company)




