#!/usr/bin/env python

import requests
import lxml
from bs4 import BeautifulSoup
from lxml import etree
from lxml import html 
import re
import argparse
import string
import time
import urllib2
import json
import os

parser = argparse.ArgumentParser(description="Scrape LinkedIn for company staff members")
parser.add_argument("-c", "--company", help="Company to search for")
parser.add_argument("-e", "--emailformat", help='Format of house email address style. Use: <fn>,<ln>,<fi>,<li> as placeholders for first/last name/initial. e.g "<fi><ln>@company.com"')
parser.add_argument("-nj", "--nojobs", help="Exclude available jobs in result", action='store_true')
parser.add_argument("-d", "--depth", help="How many pages of Yahoo to search through", default='10')
args = parser.parse_args()

found = []
emails=[]

class bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[33m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	CUSTOM = '\033[37m'


####################################################################################################
def get_elem_value(elem,css_selector,to_get):
	try:
		elem_instance = elem.cssselect(css_selector)[0]
		try:
			elem_instance_value = (elem_instance.text_content()
				if to_get == 'text' else elem_instance.get(to_get))

		except:
			#print 'two======>'
			elem_instance_value = (elem_instance.text
				if to_get == 'text' else elem_instance.get(to_get))
		
		return elem_instance_value
		# Otherwise, or on error, return ''.
	except Exception as e:
		#print('error in  get_elem_value : {}'.format(str(e)))
		return ''
####################################################################################################

####################################################################################################
def get_all_left_links_details(soup,
	search_type = "Regular",get_top_link_only=False):

	tree = html.fromstring(str(soup))
	all_left_links = list()
	try:
		all_left_links = list()
		all_left_links_divs_elems = tree.cssselect('div#web ol li')
		#print "all_left_links_divs_elems > ",len(all_left_links_divs_elems)
		for div_elem in all_left_links_divs_elems:
			left_link_dict = {'Name':'', 'Href':'', 'Text':''}
			
			left_link_dict['Name'] = get_elem_value(
				div_elem,'h3.title','text'
				)
			
			left_link_dict['Href'] = get_elem_value(
				div_elem,'h3.title a','href'
				) #changed to get href upper

			try:
				left_link_dict['Href'] = left_link_dict['Href'].replace("?trk=prof-samename-name","")
				left_link_dict['Href'] = left_link_dict['Href'].replace(
					"/url?q=","").split('&sa=')[0].replace("%20"," ").replace(
					"%3F","?").replace("%3D","=")
			except:
				pass

			#logger.info("search_type is here : {}".format(search_type))

			left_link_dict['Text'] = ( get_elem_value(
				div_elem,'p.lh-16','text'
				) if search_type == "Regular" else
				get_elem_value(
				div_elem,'p.lh-16','text'
				) )

			if left_link_dict['Name'] and left_link_dict not in all_left_links:
				all_left_links.append(left_link_dict)

			if all_left_links and get_top_link_only:
				break

	except Exception as e:
		lprint('error in  get_all_left_links_details : {}'.format(
			str(e))
		)

	return all_left_links
####################################################################################################

def formatout(companyname,emailformat):
	domain = emailformat.split("@")[1]
	if emailformat:
		print "Output file name: "+companyname+".csv"
	if not os.path.exists("Output"):
		os.makedirs("Output")
	print "_"*50
	print " "
	target = open("Output/"+companyname+".csv", 'w')
	target.write("First Name, Last Name, Company, Current Company, Title, Email, LinkedIn Url"+"\r\n")

def mangle_emails(name,company,cur_company,title,emailformat,lihref):
	target = open("Output/"+company+".csv", 'a')

	fn = string.split(name)[0]
	fi = fn[0]
	ln = string.split(name)[1]
	li = ln[0]
	full_name = fn + " " + ln
	email = emailformat.replace('<fn>',fn).replace('<ln>',ln).replace('<fi>',fi).replace('<li>',li).lower()
	email2 = filter(lambda x: x in string.printable, email)
	headers = {
	'User-Agent': 'Prowl'
	}

	if email2 not in emails:
		try:
			time.sleep(1.5)
			emails.append(email2)
			req = requests.get("https://haveibeenpwned.com/api/breachedaccount/"+email2+"?truncateResponse=true", headers=headers)
			#print "request code > ",req.content
			try:
				print "{0:30} {1:40} {2}".format(full_name, email2, req.content)
				target.write(fn+","+ln+","+company.title()+","+cur_company+","+title+","+email2+","+lihref+"\r\n")
			except Exception as e:
				print "in writing to file after request: ",str(e)
		except Exception as e:
			print "fail: ",str(e)
			emails.append(email2)
			print "{0:20} {1}".format(full_name, email2, req.content)
			print "fail"
			target.write(fn+","+ln+","+company.title()+","+cur_company+","+title+","+email2+","+lihref+"\r\n")
	else:
		pass

def search(comp,emailformat):
	depth = int(args.depth)
	print "\n"
	print bcolors.UNDERLINE + bcolors.WARNING + "S" + bcolors.OKBLUE + "T" + bcolors.OKGREEN + "A" + bcolors.ENDC + bcolors.UNDERLINE + "F" + bcolors.FAIL + "F" + bcolors.ENDC
	print "\n"
	for i in range(1,depth +1 ):
		i = str(i)
		url = 'https://uk.search.yahoo.com/search;_ylt=A9mSs3IiEdVYsUMAY6ZLBQx.;_ylu=X3oDMTEzdm1nNDAwBGNvbG8DaXIyBHBvcwMxBHZ0aWQDBHNlYwNwYWdpbmF0aW9u?p="at+{0}"+site:linkedin.com/&pz=10&ei=UTF-8&fr=yfp-t-UK317&b={1}0&pz=10&xargs=0'.format(comp,i)
		#print "search yahoo > [",url,"]"
		print bcolors.OKBLUE + "Yahoo Search > Page :"  + bcolors.FAIL + i + bcolors.ENDC + "\n"
		r = requests.get(url)
		soup = BeautifulSoup(r.text, "lxml")

		links = get_all_left_links_details(soup)

		

		for l in links:

			#print bcolors.OKGREEN + "link > "  + bcolors.WARNING + str(l) + bcolors.ENDC + "\n"

			if re.search("linkedin.com/in/", str(l['Href'])) or re.search("linkedin.com/pub/", str(l['Href'])):
				#print "linkedin.com/in/ or linkedin.com/pub/ here"
				if re.search("Top", l['Name']) or re.search(" profiles ", l['Name']):
				  #print "top here"
				  continue
					
				if  comp.lower().strip() not in l['Text'].lower().strip():
				  #print "comp  not in text"					
				  continue
					
				if l['Name'] not in found:
					#print "writing to file >",l['Name']
					div = '|'
					cut = l['Name'].split(div,1)[0]
					cut_link = l['Href'].split("linkedin.com/")[1]
					profile_link = "https://www.linkedin.com/"+str(cut_link)		
					try:
						#print "text> ",l['Text']
						title = l['Text'].lower().split('at ')[0]
						#print "title 1 > ",title
						title = title.split(".",1)[1] if "." in title else title
					except:
						title = ""
					if title:
						title = title.strip().title()
					#print "title > ",title

					try:
						if "at " in link['Name']:
							current_company  = l['Name'].lower().split('at ')[1]
						else:
							current_company  = l['Text'].lower().split('at ')[1]
						current_company = current_company.split(".",1)[1] if "." in current_company else current_company
					except:
						current_company = ""
					if current_company:
						current_company = current_company.strip().title()

					
					mangle_emails(cut, comp, current_company, title, emailformat, profile_link)
					found.append(l['Name'])
				else:
					pass
			else:
				pass


def jobs(comp):
	print bcolors.UNDERLINE + bcolors.WARNING + "J" + bcolors.OKBLUE + "O" + bcolors.OKGREEN + "B" + bcolors.ENDC + bcolors.UNDERLINE + "S"  + bcolors.ENDC
	print " "
	r = requests.get("https://www.indeed.co.uk/jobs?as_and='at+{0}'&as_phr=&as_any=&as_not=&as_ttl=&as_cmp=&jt=all&st=&salary=&radius=25&l=&fromage=any&limit=30&sort=&psf=advsrch".format(comp))
	soup = BeautifulSoup(r.text, "lxml")
	for tag in soup.findAll("h2", {"class" : "jobtitle"}):
		print tag.getText().strip()

if args.company:
	if args.emailformat:
		formatout(args.company, args.emailformat)

if args.nojobs is True:
	pass
else:
	jobs(args.company)

if args.company:
	if args.emailformat:
		search(args.company, args.emailformat)
else:
	parser.print_usage()
