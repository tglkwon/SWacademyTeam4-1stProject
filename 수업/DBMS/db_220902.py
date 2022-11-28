import sqlite3
from tkinter.tix import Select
con = sqlite3.connect('dbl.db')
cur = con.cursor()

cur.executescript('''
	DROP TABLE IF EXISTS test; 
	CREATE TABLE test
	(PK INTEGER PRIMARY KEY,
	NAME TEXT NOT NULL);
''')

cur.execute('''
	INSERT INTO test
	(PK, NAME)
	VALUES (1, "1번 데이터");
''')

# cur.lastrowid 입력 확인하는 구문

cur.execute('''
	INSERT INTO test
	(PK, NAME)
	VALUES (:pk, :name);
''', {'pk': 2, 'name' : "2번 데이터"})

cur.execute('''
	SELECT * FROM test
''')
# print(cur.fetchone())
# print(cur.fetchall())
# print(cur.fetchmany(3))

result = cur.fetchall()
print(result[0])
print(result)

con.commit() # DB에 연산 결과 반영하기

cur.executescript('''
	INSERT INTO test
	(PK, NAME)
	VALUES (3, "3번 데이터");

	INSERT INTO test
	(PK, NAME)
	VALUES (4, "4번 데이터");
''')

cur.execute('''
	UPDATE test
	SET NAME="1번 바뀐 데이터"
	WHERE PK=1
''')

con.commit() # DB에 연산 결과 반영하기

# print(cur.execute('''
# 	SELECT test
# 	WHERE NAME LIKE "1%";
# ''', {'데이터'}).fetchall())

# con.rollback() 서버 롤백 :문제 생겼을때 일정 기간 과거의 DB로 복구하는 구문

cur.executescript('''
	DROP TABLE IF EXISTS CITY; 
	CREATE TABLE CITY
	(CNO INTEGER PRIMARY KEY,
	CNAME TEXT);
		DROP TABLE IF EXISTS PART; 
	CREATE TABLE PART
	(PNO INTEGER PRIMARY KEY,
	PNAME TEXT);
		DROP TABLE IF EXISTS SUPPLIER; 
	CREATE TABLE SUPPLIER
	(SNO INTEGER PRIMARY KEY,
	SNAME TEXT);
		DROP TABLE IF EXISTS SELLS; 
	CREATE TABLE SELLS
	(SNO INTEGER NOT NULL,
	CNO INTEGER NOT NULL,
	PRICE INTEGER NOT NULL);
''')
con.commit()

# sname = "1"
# print("SUPPLIER", cur.execute('SELECT SNO FROM SUPPLIER WHERE SNAME LIKE ? LIMIT 0,1',
# 			(''.join(['%', sname, '%']),)).fetchone()
# )
# pname = "메뉴"
# print("PART", cur.execute('SELECT PNO FROM PART WHERE PNAME LIKE ? LIMIT 0,1',
# 			(''.join(['%', pname, '%']),)).fetchone()
# )
# cur.execute('''
# 	INSERT INTO SELLS VALUES(
# 	(SELECT SNO FROM SUPPLIER WHERE SNAME LIKE ? LIMIT 0,1),
# 	(SELECT PNO FROM PART WHERE PNAME LIKE ? LIMIT 0,1),
# 	?)
# ''', (''.join(['%', sname, '%']), ''.join(['%', pname, '%']), 5))

sellsList = [{'sname':2, 'pname':3, 'price': 5},
			{'sname':1, 'pname':2, 'price': 4},
			{'sname':3, 'pname':4, 'price': 7},
			{'sname':2, 'pname':3, 'price': 8},
			{'sname':4, 'pname':2, 'price': 15},
			{'sname':1, 'pname':1, 'price': 1},
			{'sname':3, 'pname':3, 'price': 3}]

cur.executemany('''
	INSERT INTO SELLS VALUES(
		(SELECT SNO FROM SUPPLIER WHERE SNAME LIKE :sname LIMIT 0,1),
		(SELECT PNO FROM PART WHERE PNAME LIKE :pname LIMIT 0,1), 
		:price)
''', sellsList)

con.commit()

result = cur.execute('''
	SELECT * FROM SELLS
	INNER JOIN SUPPLIER
	ON SUPPLIER.SNO = SELLS.SNO
''').fetchall()
print(result)

result = cur.execute('''
	SELECT B.SNAME, A.PRICE FROM SELLS AS A
	INNER JOIN SUPPLIER AS B
	ON B.SNO = A.SNO
	WHERE B.SNAME LIKE ?
''', ('%1')).fetchall()
print(result)

result = cur.execute('''
	SELECT B.SNAME, A.PRICE FROM SELLS AS A
	INNER JOIN SUPPLIER AS B
	ON B.SNO = A.SNO
	GROUP BY B.SNO
''').fetchall()
print(result)

con.commit()
con.close()
