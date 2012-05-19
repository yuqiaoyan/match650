import MySQL as mdb
import sys

try:
	con = mdb.connect('localhost','root','kddmatcher','kdd');
	cur = con.cursor()
	cur.execute("SELECT VERSION()")
	data = cur.fetchone()
	print "Database version: %s " % data

except mdb.Error, e:
	print "Error %d: %s" % (e.args[0],e.args[1])
	sys.exit(1)
finally:
	if con:
		con.close()
