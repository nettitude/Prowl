#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup
import re
import argparse
import string
import time
import json
import os
import sys
import dns.resolver
reload(sys)
sys.setdefaultencoding('utf-8')

parser = argparse.ArgumentParser(description="Scrape LinkedIn for company staff members")
parser.add_argument("-c", "--company", help="Company to search for")
parser.add_argument("-e", "--emailformat", help='Format of house email address style. Use: <fn>,<ln>,<fi>,<li> as placeholders for first/last name/initial. e.g "<fi><ln>@company.com"')
parser.add_argument("-j", "--jobs", help="Exclude available jobs in result", action='store_true')
parser.add_argument("-s", "--subdomains",  help="Find subdomains", action='store_true')
parser.add_argument("-a", "--all",  help="FIND EVERYTHING", action='store_true')
parser.add_argument("-d", "--depth", help="How many pages of Yahoo to search through", default='10')
parser.add_argument("-p", "--proxy", help="http(s)://localhost:8080", default='')
args = parser.parse_args()

found = []
emails=[]
proxies = ''
names = []
blocks = []


def proxy():
	global proxies
	proxy = args.proxy
	if proxy:
		if 'https' in proxy:
			proxies = {'https' : proxy}
		else:
			proxies = {'http': proxy}
class bcolors:
    OKGREEN = '\033[92m'
    WARNING = '\033[31m'
    FAIL = '\033[33m'

def certscanner(emailformat):
	dnsresolver = dns.resolver.Resolver()
	dnsresolver.nameservers = ['8.8.8.8']
	domain = emailformat.split("@")[1]
	company = domain.split('.', 1)[0]
	companyname = domain.split(".")[0]
	target = open("Output/"+companyname+"/domains.csv", 'w+')
	target.write("Domain, IP"+"\r\n")
	print bcolors.OKGREEN + "\nSUBDOMAINS"
	print "-"*40
	html = requests.get("https://crt.sh/?q=%."+domain+"&exclude=expired").text
	soup = BeautifulSoup(html, "lxml")
	for link in soup.findAll("a"):
		if "?id=" in link.get('href'): 
			id = link.get('href')
			cert = requests.get("https://crt.sh/"+id).text
			myregex = r'(?:[a-zA-Z0-9](?:[a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,6}'
			domains = re.findall(myregex, cert)
			for i in domains:
				if company in i:
					if i in found:
						pass
					else:
						found.append(i)
						try:
							public_ip = dnsresolver.query(i)[0]
							print bcolors.FAIL + i, public_ip
							target.write(i + "," + str(public_ip) + "\r\n")
						except:
							public_ip = ""
							print bcolors.WARNING + i
							target.write(i + "\r\n")

def formatout(companyname,emailformat):
	domain = emailformat.split("@")[1]
	companyname = domain.split(".")[0]
	if not os.path.exists("Output"):
		os.makedirs("Output")
	if not os.path.exists("Output/"+companyname):
		os.makedirs("Output/"+companyname+"/")
		target = open("Output/"+companyname+"/accounts.csv", 'w')
		target.write("First Name, Last Name, Email, Title, Profile, Breach"+"\r\n")
		target = open("Output/"+companyname+"/domains.csv", 'w')
	print "_"*50+"\n"



def bing(comp, emailformat):
	print "\n" + bcolors.OKGREEN + "BING"
	print "-"*125
	for i in range(0,40,1):
		url = 'http://www.bing.com/search?q=site:linkedin.com+works+at+'+comp+'&first='+str(i)
                res = requests.get(url)
                soup = BeautifulSoup(res.text, "lxml")
                div = ' '
                for tag in soup.findAll("li" , {"class" : "b_algo"}):
                        if re.search("linkedin.com/in/", str(tag)):
                                        if re.search("Top", tag.getText()):
                                                pass
                                        else:
                                                if tag.getText() not in blocks:
                                                        title = tag.find("h2");
                                                        cut = title.getText().split(div,2)[:2]
                                                        name = cut[0]+" "+cut[1]
                                                        time.sleep(0.1)
                                                        blocks.append(tag.getText())
                                                        if name not in names:
                                                                names.append(name)
                                                                linkedinurl = tag.find("cite").getText()
			                             		try:
									fulljob = tag.find("li").text
                                                               		mangle_emails(name, comp, emailformat, fulljob, linkedinurl)
								except:
									fulljob = ""
									mangle_emails(name, comp, emailformat, fulljob, linkedinurl)

def search(comp,emailformat):
	depth = int(args.depth)
	print "\n"
	print bcolors.OKGREEN + "YAHOO"
	print "-"*125
	for i in range(1,depth):
		i = str(i)
		try:
			r = requests.get('https://uk.search.yahoo.com/search;_ylt=A9mSs3IiEdVYsUMAY6ZLBQx.;_ylu=X3oDMTEzdm1nNDAwBGNvbG8DaXIyBHBvcwMxBHZ0aWQDBHNlYwNwYWdpbmF0aW9u?p="at+{0}"+site%3Alinkedin.com&pz=10&ei=UTF-8&fr=yfp-t-UK317&b={1}0&pz=10&xargs=0'.format(comp,i), proxies=proxies)
		except:
			print "Proxy Not Working"
			print "Exiting...."
			sys.exit(1)

		soup = BeautifulSoup(r.text, "lxml")
        	for tag in soup.findAll("div", {"class" : "dd algo algo-sr Sr"}):
			if re.search("linkedin.com/in/", str(tag)):
				if re.search("Top", tag.getText()):
					pass
				else:
					if tag.getText() not in found:
						title = tag.find("h3", {"class" : "title"});
                                                div = " "
                                                cut = title.getText().split(div,2)[:2]
                                                name = cut[0]+" "+cut[1]
						if name not in names:
							jobtext = tag.find("p", {"class" : "lh-16"});
							job = jobtext.getText()
							href = tag.find("a");
							linkpof = ""
							linkpof = href['href']
							found.append(tag.getText())
							if "View " in job:
								fulljob = " "
								mangle_emails(name, comp, emailformat, fulljob, linkpof)
							else:
								fulljob = job
								mangle_emails(name, comp, emailformat, fulljob, linkpof)

def mangle_emails(name, company, emailformat, fulljob, linkpof):
	name = name.replace(",", "")
	domain = emailformat.split("@")[1]
        companyname = domain.split(".")[0]
	target = open("Output/"+companyname+"/accounts.csv", 'a')
        fn = string.split(name)[0]
        fi = fn[0]
        ln = string.split(name)[1]
        li = ln[0]
        email = emailformat.replace('<fn>',fn).replace('<ln>',ln).replace('<fi>',fi).replace('<li>',li).lower()
        email2 = filter(lambda x: x in string.printable, email)
	headers = {
	'User-Agent': 'Prowl'
	}

	if email2 not in emails:
       		try:
			time.sleep(1.5)
			emails.append(email2)
			fulljob = fulljob.replace(",", " ")
			req = requests.get("https://haveibeenpwned.com/api/breachedaccount/"+email2+"?truncateResponse=true", headers=headers)
			breach = str(req.content)
			breach = breach.replace(",", " ")
			try:
				target.write(fn+","+ln+","+email2+","+fulljob+","+linkpof+","+breach+"\r\n")
				print "{0:30} {1:40} {2:40}".format(name, email2, fulljob[0:40])
			except:
				try:
					print "{0:30} {1:40}".format(name, email2)
					target.write(fn+","+ln+","+email2+",N/A,"+linkpof+","+breach+"\r\n")
				except:
					pass
		except:
			emails.append(email2)
			try:
				target.write(fn+"|"+ln+"|N/A|"+linkpof+"\r\n")
			except:
				pass
	else:
		pass

def jobs(comp, emailformat):
	domain = emailformat.split("@")[1]
        companyname = domain.split(".")[0]
	target = open("Output/"+companyname+"/jobs.csv", 'w')
        target.write("Job Title"+"\r\n")
	print "\n"
	print bcolors.OKGREEN + "AVAILABLE JOBS"
	print "-"*40
	r = requests.get("https://www.indeed.co.uk/jobs?as_and='at+{0}'&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius=25&l=&fromage=any&limit=30&sort=&psf=advsrch".format(comp))
	soup = BeautifulSoup(r.text, "lxml")
	for tag in soup.findAll("h2", {"class" : "jobtitle"}):
		job = str(tag.getText().encode('utf-8')).strip()
		print bcolors.FAIL + job
		target.write(job + "\r\n")
		pass

if args.proxy:
	proxy()

if args.subdomains is True:
	if args.emailformat:
		domain = args.emailformat.split("@")[1]
        	companyname = domain.split(".")[0]
                print "Output folder: "+companyname
		formatout(args.company, args.emailformat)
		certscanner(args.emailformat)
else:
	pass

if args.company:
	if args.emailformat:
		formatout(args.company, args.emailformat)

if args.jobs is True:
	jobs(args.company, args.emailformat)
else:
	pass

if args.all is True:
	certscanner(args.emailformat)
	jobs(args.company, args.emailformat)
else:
	pass

if args.company:
	if args.emailformat:
			bing(args.company, args.emailformat)
			search(args.company, args.emailformat)
else:
        parser.print_usage()
