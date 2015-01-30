import sqlite3, cgi

conn = sqlite3.connect("data.db")
c = conn.cursor()

def dropTable(tablename):
    'Drops tablename from the database'
    c.execute("DROP TABLE ?",(tablename,))
    conn.commit()
    print ("Dropped table: %s" %(tablename))

def createTable(tablename,attr):
    '''Creates a table in the database
    1st parameter - name of table (string)
    2nd parameter - Dictionary with keys and types as values'''
    L = [k[0]+' '+k[1] for k in attr]
    s = ','.join(L)
    c.execute("CREATE TABLE ?(?)",(tablename, s))
    conn.commit()
    print ("Created table %s(%s)")%(tablename, s)
    
def dropTables():
    dropTable('users')
    dropTable('trips')

def createTables():
    '(re)creates tables for users and trips'
    createTable('users', [('username','text'),('pw','text')])
    createTable('trips', [('name')])

def addUser(username,pw):
    'adds user to database'
    ## DOES NOT CHECK IF NAME ALREADY EXISTS
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO users VALUES (?,?)",(username,pw))
    print 'added user '+username

def addTrip(tripName):
    'adds trip to database'
    ## DOES NOT CHECK IF NAME ALREADY EXISTS
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO trips VALUES (?)",(tripName,))
    print 'added trip '+tripName
