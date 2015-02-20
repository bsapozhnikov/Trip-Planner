from flask import Flask,request,redirect,render_template,session,flash
import cgi, db

app=Flask(__name__)
app.secret_key = 'insert_clever_secret_here'

@app.route('/')
def root():
    if 'user' in session:
        return redirect('/home')
    else:
        return redirect('/login')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method=='GET':
        return render_template('register.html')
    else:
        username = cgi.escape(request.form['username'],quote=True)
        pw = cgi.escape(request.form['pw'],quote=True)
        if db.addUser(username,pw):
            ## flash success
            return redirect('/login')
        else:
            ## flash failure
            return redirect('/register')

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        user=cgi.escape(request.form['user'],quote=True)
        pw=cgi.escape(request.form['pass'],quote=True)
        if db.validateLogin(user,pw):
            session['user']=user
            if 'return_to' in session:
                s = session['return_to']
                session.pop('return_to',None)
                return redirect(s)
            else:
                return redirect('/home')
        else:
            ## flash invalid submission
            return redirect('/login')

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/login')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/trips/<tripID>',methods=['GET','POST'])
def trip(tripID):
    if request.method=='GET':
        tripName = db.getTrip(tripID)['tripName']
        nodes = db.getNodesByNodeID(tripID)
        nodesL=[nodes[k] for k in sorted(nodes)]
        return render_template('trip.html',tripName=tripName,nodes=nodesL)
    else:
        if 'leavingLocation' in request.form:
            lat = request.form['leavingLat']
            lng = request.form['leavingLng']
            nodes = db.getNodesByNodeID(tripID)
            if (0 not in nodes) or not (nodes[0]['nodeName'] == 'leaving'):
                db.addNode(nodeID=0,tripID=tripID,nodeName='leaving',lat=lat,lng=lng)
            else:
                db.updateNodeLocation(nodes[0]['oid'],lat,lng)
            return redirect('trips/'+tripID)
        elif 'destLocation' in request.form:
            ## ONLY WORKS IF LEAVINGLOCATION ALREADY IN DATABASE
            lat = request.form['destLat']
            lng = request.form['destLng']
            nodes = db.getNodesByNodeID(tripID)
            if (1 not in nodes) or not (nodes[1]['nodeName'] == 'dest'):
                db.addNode(nodeID=1,tripID=tripID,nodeName='dest',lat=lat,lng=lng)
            else:
                db.updateNodeLocation(nodes[1]['oid'],lat,lng)
            return redirect('trips/'+tripID)
        else:
            return 'NOT DONE YET'

@app.route('/trips')
def trips():
    return render_template('trips.html',trips=db.getTrips(session['user']))
    
@app.route('/addTrip',methods=['GET','POST'])
def addTrip():
    if request.method=='GET':
        return render_template('addTrip.html')
    else:
        tripName = cgi.escape(request.form['tripName'],quote=True)
        user = session['user']
        db.addTrip(tripName,user)
        tripID = db.getTripByUser(user,tripName)['oid']
        return redirect('trips/'+`tripID`)
    
if __name__ == '__main__':
    app.debug=True
    app.run()
