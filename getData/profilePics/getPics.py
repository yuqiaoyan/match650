import urllib

file = open("/home/yubonnie/match650/getData/professorImageURLs.csv")

i=0
for row in file:
	try:
		if(i==0):
			i+=1
			continue
		id,url = row.split(",")
		urllib.urlretrieve(url[1:len(url)-1],id[1:len(id)-1]+".jpg")
	except:
		#raise
		print "id is", id
		print "url is", url
	
