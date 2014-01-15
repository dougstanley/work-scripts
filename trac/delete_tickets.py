from trac.db.sqlite_backend import *
import sys
import os.path

try:
	trac_env = sys.argv[1]
	start = sys.argv[2]
	end = sys.argv[3]
except:
	print "Usage: remove_ticket.py TRACENV ticket_start ticket_end"
	sys.exit()

for id in xrange(int(start),int(end)+1):
	try:
		con = SQLiteConnection(os.path.join(trac_env,'db','trac.db'))
		cur = con.cursor()
		cur.execute("DELETE FROM ticket WHERE id=%s", (id,))
		cur.execute("DELETE FROM ticket_change WHERE ticket=%s",
		 (id,))
		cur.execute("DELETE FROM attachment WHERE type='ticket' and id=%s", 
		(id,))
		cur.execute("DELETE FROM ticket_custom WHERE ticket=%s", (id,))

		con.commit()
		print "Ticket #%s deleted" % id
	except Exception, e:
		print "Something went wrong,", str(e)
		con.rollback()
