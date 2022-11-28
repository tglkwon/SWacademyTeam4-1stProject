import sqlite3


con = sqlite3.connect('playlist.db')
cur = con.cursor()

cur.executescript('''
	DROP TABLE IF EXISTS T_ARTIST; 
	CREATE TABLE T_ARTIST (
		PK INTEGER PRIMARY KEY AUTOINCREMENT,
		NAME TEXT DEFAULT '이름없는 음악가'
	);
	DROP TABLE IF EXISTS T_ALBUM; 
	CREATE TABLE T_ALBUM (
		PK INTEGER PRIMARY KEY AUTOINCREMENT,
		NAME TEXT DEFAULT '이름없는 앨범',
		AFK INTEGER NOT NULL
	);
	DROP TABLE IF EXISTS T_GENRE; 
	CREATE TABLE T_GENRE (
		PK INTEGER PRIMARY KEY AUTOINCREMENT,
		NAME TEXT NOT NULL DEFAULT '이름없는 장르'
	);
	DROP TABLE IF EXISTS T_TRACK; 
	CREATE TABLE T_TRACK (
		PK INTEGER PRIMARY KEY AUTOINCREMENT,
		NAME TEXT NOT NULL DEFAULT '이름없는 트랙',
		LENGTH INTEGER DEFAULT 0,
		RATING INTEGER DEFAULT 0,
		COUNT INTEGER DEFAULT 0,
		AFK INTEGER NOT NULL,
		GFK INTEGER NOT NULL
	);
''')

singer = [('가수1',),('가수2',),('가수3',),('가수4',)]
cur.executemany('''
	INSERT INTO T_ARTIST(NAME) VALUES(?);
''', singer)
cur.execute('SELECT * FROM T_ARTIST').fetchall()
con.commit()
print(cur.lastrowid)

cur.executemany('''
	INSERT INTO T_GENRE(NAME) VALUES(?);
''', [('장르1',),('장르2',),('장르3',),('장르4',)])

album = [{'singer':'가수1','album':'앨범1'},
		{'singer':'가수2','album':'앨범2'},
		{'singer':'가수3','album':'앨범3'},
		{'singer':'가수4','album':'앨범4'}]

APK = cur.execute('SELECT PK FROM T_ARTIST WHERE NAME LIKE ?', ('%'+album[0]['singer']+'%',)).fetchone()
cur.executemany('''
	INSERT INTO T_ALBUM(NAME, AFK) 
	VALUES(:album, (SELECT PK FROM T_ARTIST WHERE NAME=:singer LIMIT 0,1));
''', album)


track = [{'album': '앨범1', 'genre': '장르4', 'title':'노래1', 'length':None, 'rating': 1, 'count': None},
		{'album': '앨범2', 'genre': '장르3', 'title':'노래2', 'length':300, 'rating': 1, 'count': 5},
		{'album': '앨범3', 'genre': '장르2', 'title':'노래3', 'length':None, 'rating': None, 'count': None},
		{'album': '앨범4', 'genre': '장르1', 'title':'노래4', 'length':278, 'rating': 1, 'count': 10},
		]

cur.executemany('''
	INSERT INTO T_TRACK(NAME, LENGTH, RATING, COUNT, AFK, GFK)
	VALUES(:title, :length, :rating, :count,
		(SELECT PK FROM T_ALBUM WHERE NAME=:album LIMIT 0,1),
		(SELECT PK FROM T_GENRE WHERE NAME=:genre LIMIT 0,1)
	);
''', track)
con.commit()

input_data = cur.execute('''
	SELECT C.NAME, B.NAME, D.NAME, A.NAME, A.LENGTH, A.RATING, A.COUNT
	FROM T_TRACK AS A
	LEFT JOIN T_ALBUM AS B
	ON B.PK=A.AFK
	LEFT JOIN T_TRACK AS C
	ON C.PK=B.AFK
	LEFT JOIN T_GENRE AS D
	ON D.PK=A.GFK
''').fetchall()

print(input_data)

con.close()