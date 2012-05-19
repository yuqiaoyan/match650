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
		return cur

	except mdb.Error, e:
		print "Error %d: %s" % (e.args[0],e.args[1])
		sys.exit(1)
	#finally:
	#	if con:
	#		con.close()

def insertProf(profDict,cur):
	cur.execute(\
		"INSERT INTO professor\
		SET	phone = %s,\
			email = %s;",\
		(profDict["phone"],profDict["email"]))	
