#create an SQLlite database and populate it with some data
import sqlite3

conn = sqlite3.connect('test.db') #connect to the database file

c = conn.cursor() #create a cursor object for the database connection object

c.execute('''CREATE TABLE IF NOT EXISTS pipe ()''') #create the table "pipe" if it doesn't exist
