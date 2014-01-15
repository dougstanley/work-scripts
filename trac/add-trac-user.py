#!/usr/bin/python
##################################################################
# I had to write this script because if you use account manager
# in trac, and set it to use SessionStore, so that account info
# is stored in the DB, then there's no way to get your initial
# account set up.
#
# This is a VERY quick and dirty hack, most of the code was copied
# from places in the account manager plugin.
# Essentially, you specify the db you're adding the user to, and
# their username/password on the command line, and it inserts them
# into the database.
#
# Once you have your initial trac admin user inserted, you can add
# additional users via the web interface.
#
# I will be attempting to get Apache to auth against Trac's db,
# and I have a feeling it won't like the digest passwords, so this
# code may have to be modified to get that to work.
####################################################################
import sys
from hashlib import md5
import psycopg2

#Some config vars
realm = "YOURREALM"
dbuser = "YOURDBUSER"
dbpass = "YOURDBPASS"
dbhost = "127.0.0.1"


#code borrowed from acct_mgr trac plugin
def _encode(*args):
	return [a.encode('utf-8') for a in args]

def htdigest(user, realm, password):
	p = ':'.join([user, realm, password])
	return md5(p).hexdigest()

def generate_hash(realm, user, password):
	user,password,realm = _encode(user, password, realm)
	return ':'.join([realm, htdigest(user, realm, password)])

#argv
# 1 = dbname
# 2 = User
# 3 = Pass
dbname,user,pw = sys.argv[1:]

hash = generate_hash(realm,user,pw)

#now connect to db and attempt to create user
dbconstr = "dbname='%s' user='%s' host='%s' password='%s'" % (dbname,dbuser,dbhost,dbpass)

sql = "INSERT INTO session_attribute (sid,authenticated,name,value) VALUES (%s,1,'password',%s)"
try:
	conn = psycopg2.connect(dbconstr)
	cur = conn.cursor()
	cur.execute(sql,(user,hash))
	conn.commit()
	conn.close()
except:
	print "Failed to do db stuff"
