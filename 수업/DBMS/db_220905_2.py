import sqlite3

con = sqlite3.connect('sns.db')
cur = con.cursor()

cur.executescript('''
	DROP TABLE IF EXISTS POST; 
	CREATE TABLE POST
	(PK INTEGER PRIMARY KEY AUTOINCREMENT,
	CONTENT TEXT);
  	DROP TABLE IF EXISTS TAG; 
	CREATE TABLE TAG
	(PK INTEGER PRIMARY KEY AUTOINCREMENT,
	NAME TEXT,
  	COUNT INTEGER DEFAULT 1);
  	DROP TABLE IF EXISTS pt; 
	CREATE TABLE pt
	(PK INTEGER PRIMARY KEY AUTOINCREMENT,
	PFK INTEGER NOT NULL,
	TFK INTEGER NOT NULL);
''')

# Psuedo 코드
# Posting  (제목, 태그들) -> 제목 입력, 태그 PK 찾아서 +1 해주고

def newPosting(title, *tags):
	print(title, tags)
	cur.execute('INSERT INTO POST(CONTENT) VALUES(?)', (title, ))
	con.commit()
	PK = cur.lastrowid()

	for tag in tags:
		cur.execute('SELECT PK FROM TAG WHERE NAME=?', (tag, ))
		try:
			# 기존에 태그가 있을때 =>
			FK = cur.fetchone()
			cur.execute('UPDATE ')
		except:
			cur.execute('INSERT INTO TAG(NAME) VALUES(?)', (tag, ))
			con.commit()
			FK = cur.lastrowid() 
		cur.execute('INSERT INTO PT(PFK, TFK), VALUES(?, ?)', (PK, FK))
		con.commit()


newPosting('제목','태그1','태그2')

# 수정 update (PK, 제목, 태그들) -> PK가 일치하는 제목 수정, 태그 PK찾아서 +-1 해주고 , PT 추가/삭제
def updatePosting(PK, title, *tags):
	cur.execute('UPDATE POST SET CONTENT=? WHERE PK=?', (title, PK))
	con.commit()

	cur.execute('SELECT TFK FROM PT WHERE PFK=?', (PK, ))
	tagList = cur.fetchall()

	newTagList = list()
	for tag in tags:
		cur.execute('SELECT PK FROM TAG WHERE NAME=?', (tag, ))
		try:
			# 기존에 태그가 있을때 => UPDATE
			FK = cur.fetchone()
			if FK is None:
				raise Exception('')

			cur.execute('UPDATE TAG SET COUNT=COUNT+1 WHERE PK=?', (fk[0], ))
		except Exception as e:
			cur.execute('INSERT INTO TAG(NAME) VALUES(?)', (tag, ))
			con.commit()
			FK = cur.lastrowid() 
		cur.execute('INSERT INTO PT(PFK, TFK), VALUES(?, ?)', (PK, FK))
		con.commit()
		newTagList.append(FK)


	for fk in tagList:
		if fk not in newTagList:
			cur.execute('UPDATE TAG SET COUNT=COUNT-1 WHERE PK=?', (fk[0], ))
			cur.execute('DELETE FROM PT WHERE PFK=? AND TFK=?' (PK, fk[0]))
			con.commit()


updatePosting(1, '제목1', '태그1', '태그4')

def postingList():
	cur.execute('''
		SELECT A.PK A.CONTENT, C.NAME, C.COUNT FROM POST AS A
		LEFT JOIN PT AS B
		ON A.PK=B.PFK
		LEFT JOIN TAG AS C
		ON C.PK=B.TFK
	''')
	return cur.fetchall()


# postingList()