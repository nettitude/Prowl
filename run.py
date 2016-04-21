from bs4 import BeautifulSoup
import urllib2
import sys
import string
import argparse
from colorama import Fore, Back, Style
from colorama import init
import os

print "code updated"

URLS = []
found = []

parser = argparse.ArgumentParser(description="Scrape LinkedIn for staff members")
parser.add_argument("-c", "--company", help="Company to search for")
parser.add_argument("-e", "--emailformat", help='Format of house email address style. Use: <fn>,<ln>,<fi>,<li> as placeholders for first/last name/initial. e.g "<fi><ln>@company.com"')
args = parser.parse_args()

def greppage(company, emailformat):
	global URLS
	for i in URLS:
		request_headers = {
		"Accept-Language": "en-US,en;q=0.5",
		"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
		"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		"Connection": "keep-alive" }
		try:
			request = urllib2.Request(i, headers=request_headers)
			contents = urllib2.urlopen(request).read()
		except KeyboardInterrupt:
			sys.exit(0)
		except urllib2.HTTPError, e:
    			print "BLOCKED BY LINKEDIN"
		except urllib2.URLError, e:
    			print "BLOCKED BY LINKEDIN"
		except httplib.HTTPException, e:
    			print "BLOCKED BY LINKEDIN"
		try:
			soup = BeautifulSoup(contents, "lxml")
			for td in soup.findAll("li", { "class":"profile-card" }):
				link = td.find('a')['href'].lower()
				for g in td.findAll('a'):
            				name = g.getText()
          			else:
            				pass
          			for f in td.findAll('p'):
            				profile = f.getText().lower()
				if company in profile:
					if link not in URLS:
						URLS.append(link)
						if name+profile not in found:		
							found.append(name+profile)
							if emailformat:
								mangle_emails(name, company, emailformat, profile)
							else:
								print name + "," + profile
		except:
			pass
def search(companyname, emailformat):
	formatout(companyname, emailformat)
	global URLS
	emailformat
	companyname = companyname.lower()
	header = {'User-Agent': 'Mozilla/5.0'}
	req = urllib2.Request("https://uk.search.yahoo.com/search?p=profile%20"+companyname.replace(" ", "%20")+"%20linkedin.com/")
	page = urllib2.urlopen(req)
  	soup = BeautifulSoup(page, "lxml")
	company = soup.findAll("h3", {"class" : "title"})	
	print(Fore.GREEN + "################# FOUND ACCOUNTS #################" + Style.RESET_ALL)
	for i in company:
		c = i.find("a")
		href = c['href']
		if "linkedin.com/in/" in href:
			print href
			URLS.append(href)
		if "linkedin.com/pub/" in href:
			print href
			URLS.append(href)
	print(Fore.GREEN + "##################################################" + Style.RESET_ALL)
	greppage(companyname, emailformat)


def formatout(companyname,emailformat):
	if emailformat:
		print "Output file name: "+emailformat.split("@")[1]+".txt"
def mangle_emails(name, company, emailformat, profile):
	target = open("Output/"+company+".txt", 'a')
	fn = string.split(name)[0]
	fi = fn[0]
	ln = string.split(name)[1]
	li = ln[0]
	email = emailformat.replace('<fn>',fn).replace('<ln>',ln).replace('<fi>',fi).replace('<li>',li).lower()
	email2 = filter(lambda x: x in string.printable, email)
	print name + "," + profile + "," + email2
	target.write(email2+"\n")
	


if args.company:
	search(args.company, args.emailformat)
else:
	parser.print_usage()
