#!/usr/bin/env python

from bs4 import BeautifulSoup
import urllib2
import sys
import string
import argparse
import socket
import dns.resolver
import os
import json
from random import randint
from time import sleep

URLS = []
found = []

parser = argparse.ArgumentParser(description="Scrape LinkedIn for company staff members")
parser.add_argument("-c", "--company", help="Company to search for")
parser.add_argument("-e", "--emailformat", help='Format of house email address style. Use: <fn>,<ln>,<fi>,<li> as placeholders for first/last name/initial. e.g "<fi><ln>@company.com"')
parser.add_argument("-p", "--profile", help="LinkedIn profile account to start with")
parser.add_argument("-s", "--subdomain", help='Optional - LinkedIn subdomain used in target company country. e.g "au", "uk" (Default None)', default="")
args = parser.parse_args()

def greppage(company, emailformat):
	print '\033[1;42mEmail Addresses Found              \033[0;m'
	global URLS
	for i in URLS:
		try:
			sleep(randint(0,1))
			from pyvirtualdisplay import Display
			from selenium import webdriver
			display = Display(visible=0, size=(800, 600))
			display.start()
			browser = webdriver.Firefox()
			browser.get(i)
			contents = browser.page_source
			browser.quit()
			display.stop()

		except KeyboardInterrupt:
			sys.exit(0)
		except:
			#print contents
			pass	
	
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

def search(companyname, emailformat, subdomain):
	formatout(companyname, emailformat)
	global URLS
	emailformat
	companyname = companyname.lower()
	if subdomain != "":
		subdomain = subdomain + "."
	header = {'User-Agent': 'Mozilla/5.0'}
	# TODO: Add support for other Yahoo subdomains - Works okay for companies outside of UK the time being though
	search_url = "https://uk.search.yahoo.com/search?p=" + companyname.replace(" ", "%20") + "%20" + subdomain + "linkedin.com"
	# print search_url
	req = urllib2.Request(search_url)
	page = urllib2.urlopen(req)
  	soup = BeautifulSoup(page, "lxml")
	company = soup.findAll("h3", {"class" : "title"})
	print ""
	try:
		for i in company:
			c = i.find("a")
			href = c['href']
			if "linkedin.com/in/" in href:
				URLS.append(href)
			if "linkedin.com/pub/" in href:
				URLS.append(href)
			if "linkedin.com%2fin%2f" in href:
				URLS.append(href)
			if "linkedin.com%2fpub%2f" in href:
				URLS.append(href)
	except:
		pass
	greppage(companyname, emailformat)

def formatout(companyname,emailformat):
	domain = emailformat.split("@")[1]
	if emailformat:
		print "Output file name: "+emailformat.split("@")[1]+".txt"
	if not os.path.exists("Output"):
		os.makedirs("Output")
	dns_enum(domain)
def mangle_emails(name, company, emailformat, profile):
	target = open("Output/"+company+".txt", 'a')
	fn = string.split(name)[0]
	fi = fn[0]
	ln = string.split(name)[1]
	li = ln[0]
	email = emailformat.replace('<fn>',fn).replace('<ln>',ln).replace('<fi>',fi).replace('<li>',li).lower()
	email2 = filter(lambda x: x in string.printable, email)
	try:
		req = urllib2.urlopen("https://haveibeenpwned.com/api/breachedaccount/"+email2+"?truncateResponse=true")
		data = json.load(req)
        	try:
			print name + ' | ' + profile + ' | ' + email2 + ' | ' + "\033[1;41m"+ ", ".join(data) +"\033[0;m"
			out = email2 + "	" +", ".join(data)
			target.write(out+"\r\n")
		except:
			pass
	except:
		print name + " | " + profile + " | " + email2
		target.write(email2+"\r\n")

def dns_enum(domain):
	print '\033[1;42mMX Records                         \033[0;m'
	answers = dns.resolver.query(domain, 'MX')
	for rdata in answers:
  		print rdata.exchange
if args.company:
        if args.profile:
                URLS.append(args.profile)
        search(args.company, args.emailformat, args.subdomain)
else:
	parser.print_usage()
