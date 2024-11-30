from flask import Flask, request, render_template, session, redirect, url_for
import sqlite3
from functools import wraps
from datetime import datetime
from datetime import timedelta
import secrets
from hashlib import sha256


app = Flask(__name__)
DBNAME = "tracker.db"
app.secret_key = secrets.token_hex(32)

# session renewal
app.permanent_session_lifetime = timedelta(days=7)

def login_required(f):
	@wraps(f)
	def decorated_function(*args, **kwargs):
		if 'user' in session:
			return f(*args, **kwargs)
		return render_template("login.html")
	return decorated_function

@app.route('/login', methods=['POST'])
def login():
	if 'user' in session:
		return redirect(url_for('index'))
	user = request.form['username']
	password = request.form['password']
	h_password = sha256(password.encode('utf-8')).hexdigest())

	if user == "tugberk" and h_password == "3a57c3967d5b881260c6345d117546ea1e7b0497a5b8cee41c576bb961b02f64":
		session['user'] = user
		session.permanent = True #so user is not asked to reenter
		return redirect(url_for('index'))
	elif user == "hande" and h_password == "a9e28f3f8ba4d14a0f322aad2422a300c7131b9ee057218965953b8e460519db":
		session['user'] = user
		session.permanent = True
		return redirect(url_for('index'))
	else:
		return "404"

@app.route('/')
@login_required
def index():
	user = session['user']
	try:
		data = getTotals(user)
		#print(data)
		moves = getMovements(user)
		return render_template("index.html", data=data, moves=moves)
	except:
		return render_template("index.html", data="data yok")
	


@app.route('/ekle',methods=['POST'])
@login_required
def ekle():
	hareket = request.form['hareket']
	adet = request.form['adet']
	username = session['user']
	addToDatabase(username, hareket, adet)
	return redirect(url_for('index'))

@app.route('/detay/<move>')
@login_required
def detay(move):
	user = session['user']
	data = getDetay(user, move)
	return render_template("detay.html", data=data, header=move)

'''
jjacks 100
squats 120
pusuhp 20
'''

#helpers
def getTotals(username):
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	cur.execute('select hareket, sum(adet) as toplam from tracker where user is ? group by hareket', (username, ))
	data = cur.fetchall()
	return data

#get detay
def getDetay(username, move):
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	cur.execute("select tarih, adet from tracker where hareket is ? and user = ?", (move,  username))
	data = cur.fetchall()
	return data

#get movements
def getMovements(username):
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	cur.execute('select hareket from tracker where user is ? group by hareket', (username, ))
	data = cur.fetchall()
	return data

#add a movement to database
def addToDatabase(username, hareket, adet):
	#tarih = datetime.datetime.now()
	tarih = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	#print(username, hareket, adet)
	cur.execute("insert into tracker(user,tarih,hareket,adet) values(?,?,?,?)", (username, tarih, hareket, adet))
	conn.commit()
	conn.close()
	return


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=8081, debug=True)
