import sqlite3
import datetime


conn = sqlite3.connect("tracker.db")
cur = conn.cursor()

cur.execute('create table if not exists tracker( id INTEGER PRIMARY KEY AUTOINCREMENT, user TEXT NOT NULL, tarih TEXT NOT NULL, hareket TEXT NOT NULL, adet INTEGER NOT NULL)')

conn.commit()

def ekle(tarih,hareket, adet):
	#tarih = datetime.datetime.now()
	cur.execute("insert into tracker(user,tarih,hareket,adet) values(?, ?,?,?)", ("tugberk",tarih,hareket, adet))
	conn.commit()
	print("record added")

def view():
	#cur.execute("select * from tracker")
	#cur.execute("select hareket, sum(adet) from tracker group by hareket")
	cur.execute("select hareket, tarih, adet from tracker where hareket = ?", ("squat",))
	records = cur.fetchall()
	print(records)
'''
ekle("squat",10)
ekle("sinav",40)
ekle("sinav",40)
view()
'''
#ekle("2024-11-07","squat",30)
#ekle("2024-11-09","squat",30)
view()

cur.close()
conn.close()
