from flask import Flask, request, render_template, session, redirect, url_for
import sqlite3
from functools import wraps
from datetime import datetime

app = Flask(__name__)

DBNAME = "tracker.db"

@app.route('/')
def index():
	data = getTotals()
	moves = getMovements()
	return render_template("index.html", data=data, moves=moves)


@app.route('/ekle',methods=['POST'])
def ekle():
	hareket = request.form['hareket']
	adet = request.form['adet']
	addToDatabase(hareket, adet)
	return redirect(url_for('index'))

@app.route('/detay/<move>')
def detay(move):
	data = getDetay(move)
	return render_template("detay.html", data=data, header=move)


#helpers
def getTotals():
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	cur.execute('select hareket, sum(adet) as toplam from tracker group by hareket')
	data = cur.fetchall()
	return data

#get detay
def getDetay(move):
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	cur.execute("select tarih, adet from tracker where hareket is ?", (move, ))
	data = cur.fetchall()
	return data

#get movements
def getMovements():
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	cur.execute('select hareket from tracker group by hareket')
	data = cur.fetchall()
	return data

#add a movement to database
def addToDatabase(hareket, adet):
	#tarih = datetime.datetime.now()
	tarih = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	conn = sqlite3.connect(DBNAME)
	cur = conn.cursor()
	cur.execute("insert into tracker(tarih,hareket,adet) values(?,?,?)", (tarih, hareket, adet))
	conn.commit()
	conn.close()
	return


if __name__ == "__main__":
	app.run(debug=True)
