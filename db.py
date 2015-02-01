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
    dropTable('nodes')

def createTables():
    '(re)creates tables for users and trips'
    createTable('users', [('username','text'),('pw','text')])
    createTable('trips', [('name','text'),('user','text'),('numNodes','integer')])
    createTable('nodes', [('nodeID','integer'),('tripID','integer'),('nodeName','text'),('lat','text'),('lng','text')])

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
def getTrip(tripID):
    'returns trip with given oid as a dictionary'
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    for row in c.execute("SELECT oid,* FROM trips WHERE oid=?",(tripID,)):
        content = {'tripName':row[1],'username':row[2],'numNodes':row[3]}
        return content

def getTripByUser(username,tripName):
    '''returns trip with given user and name as a dictionary
    also includes the oid'''
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    for row in c.execute("SELECT oid,* FROM trips WHERE user=? AND name=?",(username,tripName)):
        content = {'oid':row[0],'tripName':row[1],'username':row[2],'numNodes':row[3]}
        return content
    
def getTrips(username):
    '''returns all of user's trips as a dictionary
    the key is the oid
    the value is a dictionary containing threst of the data (placename)'''
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    trips = {}
    for row in c.execute("SELECT oid,* FROM trips WHERE user=?",(username,)):
        content = {'tripName':row[1],'username':row[2],'numNodes':row[3]}
        trips[row[0]]=content
    return trips
    
def addTrip(tripName,username):
    'adds trip to database'
    ## DOES NOT CHECK IF NAME ALREADY EXISTS
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO trips VALUES(?,?,0)",(tripName,username))
    conn.commit()
    print "added %s's trip %s"%(username,tripName)

def incTripNumNodes(tripID):
    'increments the numNodes variable in trip with given oid'
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("UPDATE trips SET numNodes = numNodes + 1 WHERE oid=?",(tripID,))
    conn.commit()
    print "Trip %i has one more node"%int(tripID)

def decTripNumNodes(tripID):
    'decrements the numNodes variable in trip with given oid'
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("UPDATE trips SET numNodes = numNodes - 1 WHERE oid=?",(tripID,))
    conn.commit()
    print "Trip %i has one less node"%tripID

def getNodesByOID(tripID):
    '''returns all of trip's nodes as a dictionary
    the key is the node's oid
    the value is a dictionary containing the rest of the data (nodeID, tripID, lat, lng)'''
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    nodes = {}
    for row in c.execute("SELECT oid,* FROM nodes WHERE tripID=?",(tripID,)):
        content = {'nodeID':row[1],'tripID':row[2],'nodeName':row[3],'lat':row[4],'lng':row[5]}
        nodes[row[0]]=content
    return nodes

def getNodesByNodeID(tripID):
    '''returns all of trip's nodes as a dictionary
    the key is the node's nodeID
    the value is a dictionary containing the rest of the data (oid, tripID, lat, lng)'''
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    nodes = {}
    for row in c.execute("SELECT oid,* FROM nodes WHERE tripID=?",(tripID,)):
        content = {'oid':row[0],'tripID':row[2],'nodeName':row[3],'lat':row[4],'lng':row[5]}
        nodes[row[1]]=content
    return nodes    
        
def addNode(tripID,nodeName='',lat='',lng=''):
    'adds node to given trip'
    nodeID = getTrip(tripID)['numNodes']
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("INSERT INTO nodes VALUES(?,?,?,?,?)",(nodeID,tripID,nodeName,lat,lng))
    conn.commit()
    incTripNumNodes(tripID)
    print "Added Node %i to Trip %i"%(nodeID,tripID)

def updateNodeLocation(oid,lat,lng):
    'updates the lat and lng values for the node with the given oid'
    conn = sqlite3.connect('data.db')
    c = conn.cursor()
    c.execute("UPDATE nodes SET lat = ? WHERE oid=?",(lat,oid))
    c.execute("UPDATE nodes SET lng = ? WHERE oid=?",(lng,oid))
    conn.commit()
    print "Set Node's location to (%d,%d)"%(float(lat),float(lng))
