import MySQLdb as mdb
import sys

#CONFIGURATIONS#
host	= 'localhost'
user	= 'root'
pwd	= 'kddmatcher'
db	= 'kdd'

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
			interest = %s" % 
		(profDict["phone"],profDict["email"],profDict["homepage"],\
		profDict["position"],profDict["affiliation"],profDict["address"],\
		profDict["phduniv"],profDict["phdmajor"],profDict["bsuniv"],\
		profDict["bio"],profDict["pictureURL"],profDict["coauthorID"],\
		profDict["interest"]))
	con.commit()	
