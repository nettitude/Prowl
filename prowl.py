#Importing Libs##########
from bs4 import BeautifulSoup
import urllib2
from itertools import izip
import string
#########################

URLS = []
EMAILS = []
GOOGLE = []

target = open("output.txt", 'w')
q=0
global fill
 
#Menu####################
while True:
	print (30 * '-')
	print ("   M A I N - M E N U")
	print (30 * '-')
	print ("1. Grab Linkedin Data")
	print ("2. Email Enumeration")
	print ("3. Username Enumeration")
	print (30 * '-')
	 
	## Get input ###
	choice = raw_input('')
	 
	### Convert string to int type ##
	choice = int(choice)
	 
	### Take action as per selected menu-option ###
	if choice == 1:
		
		print ("4. Basic")
		print ("5. Deep & Thorough")
		print (30 * '-')
		## Get input ###
		submenu2 = raw_input('Enter your choice [1-3] : ')
		### Convert string to int type ##
		submenu2 = int(submenu2)

		### Take action as per selected menu-option ###
		if submenu2 == 4:
			#Defining Search Variables
			link = raw_input("Enter Base Linkedin Profile: ")
			Org = raw_input("What company are you searching for?: ")
			Org2 = Org.lower()

			##########################

			print "---------------------------------------"
			print "Searching for " + Org
			print "----------------------------------------"

			def greppage(link, Org, URLS):

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
					global sdf
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
						if Org2 in item[1]:	
							if item[2] not in URLS:
								print item[0]+ "	" + item[1]+ "	" +item[2]
								URLS.append(item[2])
								EMAILS.append(item[0])
								pre=(item[0]+ "	" + item[1]+ "	" +item[2])
								sdf = filter(lambda x: x in string.printable, pre)
								PRINT.append(sdf)
								#print sdf
								target.write(sdf + "\n")			
					x+=1

			greppage(link, Org, URLS)

			for iturl in URLS:
				greppage(iturl, Org, URLS)
				# for full in PRINT:
					# q+=1
					# s = str(q) + ": " + full
					# #print s
					# target.write(s + "\n")
					# #print URLS        



		elif submenu2 == 5:
				#Defining Search Variables
				link = ""
				Org = raw_input("What company are you searching for?: ")
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

				def greppage(link, Org, URLS):

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
						global sdf
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
							if Org2 in item[1]:	
								if item[2] not in URLS:
									print item[0]+ "	" + item[1]+ "	" +item[2]
									URLS.append(item[2])
									EMAILS.append(item[0])
									pre=(item[0]+ "	" + item[1]+ "	" +item[2])
									sdf = filter(lambda x: x in string.printable, pre)
									PRINT.append(sdf)
									#print sdf
									target.write(sdf + "\n")			
						x+=1

				for link in GOOGLE:
					#print link
					if "linkedin.com/pub/" or "linkedin.com/in/" in link:
						greppage(link, Org, URLS)
						for iturl in URLS:
							greppage(iturl, Org, URLS)
							# for full in PRINT:
								# q+=1
								# s = str(q) + ": " + full
								# #print s
								# target.write(s + "\n")
								# #print URLS  
					else:
						print "non-company link"

				GOOGLE = []


	elif choice == 2:
		emailhost = "@" + raw_input("What is the organisations hostname?: ")

		print (30 * '-')
		print ("1: firstname + lastname@" + emailhost)
		print ("2: firstname + . + lastname@" + emailhost)
		print ("3: lastname + firstname@" + emailhost)
		print ("4: lastname + . + firstname@" + emailhost)
		print ("5: firstname - firstletter + lastname@" + emailhost)
		print ("6: lastname + firstname - firstletter@" + emailhost)
		print ("7: lastname - firstletter + firstname@" + emailhost)
		print ("8: firstname + lastname - lastletter@" + emailhost)

		print (30 * '-')
		 
		## Get input ###
		choice = raw_input('Enter your choice : ')
		 
		### Convert string to int type ##
		choice = str(choice)
		 
		### Take action as per selected menu-option ###
		if choice == "1":
		        for i in EMAILS:
	        		prefix = i.split()
	        		print prefix[0]+prefix[1]+emailhost
		elif choice == "2":
		        print "firstname+.+lastname@" + emailhost
		        for i in EMAILS:
		        	prefix = i.split()
		        	print prefix[0]+ "." + prefix[1]+emailhost
		elif choice == "3":
		        print "lastname+firstname@" + emailhost
			for i in EMAILS:
		        	prefix = i.split()
		        	print prefix[1]+prefix[0]+emailhost
		elif choice == "4":
		        print "lastname+.+firstname@" + emailhost
		        for i in EMAILS:
		        	prefix = i.split()
		        	print prefix[1]+ "." + prefix[0]+emailhost
		elif choice == "5":
		        print "firstname-firstletter+lastname@" + emailhost
		        for i in EMAILS:
		        	prefix = i.split()
		        	print prefix[0][0]+ "." + prefix[1]+emailhost
		elif choice == "6":
		        print "lastname+.+firstname-firstletter@" + emailhost
		        for i in EMAILS:
		        	prefix = i.split()
		        	print prefix[1]+ "." + prefix[0][0]+emailhost
		elif choice == "7":
		        print "lastname-firstletter+firstname@" + emailhost
		        for i in EMAILS:
		        	prefix = i.split()
		        	print prefix[1][0]+ "." + prefix[0]+emailhost
		elif choice == "8":
		        print "firstname+.+lastname-firstletter@" + emailhost
		        for i in EMAILS:
		        	prefix = i.split()
		        	print prefix[0]+ "." + prefix[1][0]+emailhost

		else:    ## default ##
		        print ("Invalid number. Try again...")
	elif choice == 3:
	        print ("Rebooting the server...")
	else:    ## default ##
	        print ("Invalid number. Try again...")
	###########################



