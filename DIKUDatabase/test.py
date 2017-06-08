import os
import sqlite3

def add():
	db = get_db()
	db.execute('insert into course values ("hello",100)')
	db.commit()
	list = db.execute('select * from course')
	print "hello"
