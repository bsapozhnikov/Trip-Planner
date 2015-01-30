from flask import Flask,request,redirect,render_template,session,flash
import cgi

app=Flask(__name__)
app.secret_key = 'insert_clever_secret_here'

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        user=cgi.escape(request.form['user'],quote=True)
        pw=cgi.escape(request.form['pass'],quote=True)
        if True: ## validate user
            session['user']=user
            if 'return_to' in session:
                s = session['return_to']
                session.pop('return_to',None)
                return redirect(s)
            else:
                return redirect('/home') ## redirect to default home page
        else:
            pass ## invalid submission

@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/login')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/trip/<tripName>')
def trip(tripName):
    return render_template('trip.html',tripName=tripName)
    
@app.route('/addTrip',methods=['GET','POST'])
def addTrip():
    if request.method=='GET':
        return render_template('addTrip.html')
    else:
        tripName = cgi.escape(request.form['tripName'],quote=True)
        return redirect('trip/'+tripName)
    
if __name__ == '__main__':
    app.debug=True
    app.run()
