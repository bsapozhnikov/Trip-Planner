import sqlite3, cgi

conn = sqlite3.connect("data.db")
c = conn.cursor()

### TABLE MANAGER STUFF ###
def dropTable(tablename):
    'Drops tablename from the database'
    c.execute("DROP TABLE %s"%(tablename))
    conn.commit()
    print ("Dropped table: %s" %(tablename))

def createTable(tablename,attr):
    '''Creates a table in the database
    1st parameter - name of table (string)
    2nd parameter - Dictionary with keys and types as values'''
    L = [k[0]+' '+k[1] for k in attr]
    s = ','.join(L)
    c.execute("CREATE TABLE %s(%s)"%(tablename, s))
    conn.commit()
    print ("Created table %s(%s)")%(tablename, s)
    
def dropTables():
    dropTable('users')
    dropTable('trips')

def createTables():
    '(re)creates tables for users and trips'
    createTable('users', [('username','text'),('pw','text')])
    createTable('trips', [('name','text'),('user','text')])

### USER MANAGER STUFF ###
def getUsers():
    '''returns dictionary of users:
    the key is the username
    the value is a dictionary containing the rest of the data (the pw)'''
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    users = {}
    for row in c.execute("SELECT * FROM users"):
        content = {'pw':row[1]}
        users[row[0]]=content
    return users

def getUser(username):
    '''returns user as a dictionary'''
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    user = {}
    for row in c.execute("SELECT * FROM users WHERE username=?",(username,)):
        user['pw'] = row[1]
    return user

def userExists(username):
    '''returns True if user already exists, false otherwise'''
    return username in getUsers().keys()

def validateLogin(username,pw):
    '''return True if there exists given user with given pw, false otherwise'''
    return userExists(username) and (getUser(username)['pw'] == pw)
    
def addUser(username,pw):
    '''tries to add user to database
    return true if successful, false otherwise'''
    if userExists(username):
        print 'username already exists'
        return False
    else:
        conn = sqlite3.connect('data.db')
        c = conn.cursor()
        c.execute("INSERT INTO users VALUES(?,?)",(username,pw))
        conn.commit()
        print 'added user '+username
        return True
        
### TRIP MANAGER STUFF ###
def getTrips(username):
    '''returns all of user's trips as a dictionary
    the key is the placename
    the value is a dictionary containing threst of the data (nothing)'''
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    trips = {}
    for row in c.execute("SELECT * FROM trips WHERE user=?",(username,)):
        content = {}
        trips[row[0]]=content
    return trips
    
def addTrip(tripName,username):
    'adds trip to database'
    ## DOES NOT CHECK IF NAME ALREADY EXISTS
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO trips VALUES(?,?)",(tripName,username))
    conn.commit()
    print "added %s's trip %s"%(username,tripName)
