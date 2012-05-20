import MySQLdb as mdb
import sys
from build_indexing import *

#CONFIGURATIONS#
host	= 'localhost'
user	= 'root'
pwd	= 'kddmatcher'
db	= 'kdd'
jsonPath= 'committees'
profKeys= ["Phone","Email","Homepage","Position","Affiliation","Address","Phduniv","Phdmajor","Bsuniv","Bio","PictureURL","CoauthorID","Interest"]

def connectDB():
#returns a cursor object to our database
	try:
		con = mdb.connect(host,user,pwd,db)
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
			arnetID = %s",  
		(profDict["Phone"],profDict["Email"],profDict["Homepage"],\
		profDict["Position"],profDict["Affiliation"],profDict["Address"],\
		profDict["Phduniv"],profDict["Phdmajor"],profDict["Bsuniv"],\
		profDict["Bio"],profDict["PictureURL"],profDict["CoauthorID"],\
		profDict["Interest"],profDict["Id"]))
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

def getInsertData():
#main function to get professor data
#and insert into the database

	con, cur = connectDB()

	file = open("committees")
	i = 0
	for line in file:
		if(i > 2):
			break
		i+=1
		rawDict = parseJSONLine(line)		
		#ToDo: grab interest data
		rawDict["Interest"] = get_interest_by_id(str(rawDict["Id"]))
		print "interest is",rawDict["Interest"]
#ToDo: check that interest data exists
#ToDo: if interest data, does not exist, then do not add to DB
# else 
#ToDo: grab coauthor data
		#convert dict to a well formed dictionary
		#all keys in profKeys must exist in dict
		profDict = rawDictToProfDict(rawDict)

		#add professor to DB
		#insertProf(profDict,cur,con)

	file.close()
		
