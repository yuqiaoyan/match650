import re
import MySQLdb as mdb
import sys
from build_indexing import *

#PATTERNS#
interestPat = re.compile("[a-zA-Z]+",re.IGNORECASE)

#CONFIGURATIONS#
#host	= 'http://ec2-107-20-36-41.compute-1.amazonaws.com/'
host	= 'localhost'
user	= 'root'
pwd	= 'kddmatcher'
db	= 'kdd'
jsonPath= 'committees'
profKeys= ["Phone","Email","Homepage","Position","Affiliation","Address","Phduniv","Phdmajor","Bsuniv","Bio","PictureURL","CoauthorID","Interest"]

def connectDB():
#returns a cursor object to our database
	try:
		con = mdb.connect(host,user,pwd,db,use_unicode=True,charset = "utf8")
		cur = con.cursor()
		return con,cur

	except mdb.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)
	#finally:
	#	if con:
	#		con.close()

def insertProf(profDict,cur,con):
#profDict must have all fields for the insert 
	try:
		cur.execute(\
			"INSERT INTO professor\
			SET	phone = %s,\
				email = %s,\
				homepage = %s,\
				position = %s,\
				affiliation = %s,\
				address = %s,\
				phduniv = %s,\
				phdmajor = %s,\
				bsuniv = %s,\
				bio = %s,\
				pictureURL = %s,\
				coauthorID = %s,\
				interest = %s,\
				arnetID = %s,\
				name = %s",  \
			(profDict["Phone"],profDict["Email"],profDict["Homepage"],\
			profDict["Position"],profDict["Affiliation"],profDict["Address"],\
			profDict["Phduniv"],profDict["Phdmajor"],profDict["Bsuniv"],\
			profDict["Bio"],profDict["PictureUrl"],profDict["CoauthorID"],\
			profDict["Interest"],profDict["Id"],profDict["Name"]))
	except Exception as err:
		print type(err)
		print(err.args)
		print "professor is ", profDict
	con.commit()	

def rawDictToProfDict(rawDict):
#given the raw JSON Dict from Arnetminer
#convert it to a well formed professor dictionary
	for key in profKeys:
		if key not in rawDict.keys():
			rawDict[key] = None
	return rawDict


def parseJSONLine(text):
	data = json.loads(text)
	return(data[0])

def isValidInterest(text):
#returns true if the text contains at least 1 char a-zA-Z
	if not text:
		return False
	if(len(interestPat.findall(text)) > 0):
		return True
	return False

def getArnetData(coID):
#get professor data from Arnetminer API through ID
# and return the response as a dictionary
	url = "http://arnetminer.org/services/person/"
	url = url + coID + "?u=oyster&o=tff"
	jsonString = urllib.urlopen(url)
	profDict = json.loads(jsonString)[0]
	return profDict
 
def getInsertData():
#main function to get professor data
#and insert into the database

	con, cur = connectDB()

	file = open("newcoauthorIDs_6_17.csv")
	for coid in file:
		rawDict = getArnetData(coid) 		
		#ToDo: grab interest data
		rawDict["Interest"] = get_interest_by_id(str(rawDict["Id"]))
	
		#if Interest is not valid, do not add to DB
		if not isValidInterest(rawDict["Interest"]): continue
		#get coauthorIDs as string
		rawDict["CoauthorID"]= get_coAuthorIds_by_id(str(rawDict["Id"]))

		#convert dict to a well formed dictionary
		#all keys in profKeys must exist in dict
		profDict = rawDictToProfDict(rawDict)

		#add professor to DB
		insertProf(profDict,cur,con)

	file.close()
		
