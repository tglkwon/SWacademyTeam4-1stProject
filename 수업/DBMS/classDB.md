## class pm DBMS 류기군 선생님 - 관계형 DB
### 데이터베이스 개요
data를 DB(Hadoop, spark)에 저장해서 통계를 이용해 분석해서 model화 한다. 그런데 현대는 다루는 data의 크기가 상상을 초월해서 그 자체를 다루는 것이 어려워짐. 
관계형 DB을 앞으로 공부하게 될것
데이터 전체중 80%가 비정형 데이터이다. 영상, 자연어처리-텍스트, 음성
데이터 레이크 하우스로 통째로 다 모으는 것이 요즘 대세

-data base - dbms
특정 조건에 맞춰서 정리된 데이터의 모음, 그리고 그것을 관리하는 시스템

-data : 처리되지 않은 자료의 모음
-text, numbers, images, audio, video

-information : 처리된(계산된) 데이터
-documents, audio, images, video

-db의 특징
	-실시간 접근성
	-계속적인 변화 
	-동시 공유 가능
	-내용에 의한 참조 가능

-dbms : 데이터베이스들을 관리하고 사용자 설정 등 관리를 용이하게 해주는 시스템
	-create databases
	-insert, update and delete data
	-sort and query data
	-create form and report

-dbms의 종류
	-계층형 모델
	-네트워크형 모델
	-관계데이터 모델 - mysql, mariadb, postgre 등등
	-객체 관계 모델(ORM)

-RDMS : 관계형 데이터베이스 매니저 시스템
	데이터 안정성 safety
	동시 접근성 cocurrent access
	장애 허용성 fault tolerance - 롤백해서 복구함
	데이터 무결성 integrity
	데이터 확장성 scalability
	데이터 보고서 reporting

-RDMS concepts
	relation - table
	tuple - row or record
	attribute - column or field
	cardinality - Number of rows
	Degree - number of columns
	domain - pool or legal values
	prime key - unique identifier


### 데이터베이스 설계
개체 관계 모델(Entity-Relationship Model)
개체 (entity) : 실 세계에 존재하는 분리된 실체 하나를 표현, 일반적으로 명사 하나에 해당
관계 (relationship) : 개체들 사이에 존재하는 연관이나 연결, 일반적으로 동사에 해당, 최대 대응수와 최소 대응수로 구성
속성 (attribute) : 개체의 성질, 분류, 식별, 수량, 상태 등을 나타내느 세부 항목, 관계또한 속성을 보유할 수 있음
기본키 (primary key) : 모든 개체를 고유하게 식별할 수 있는 속성


### SQL
Structured Query Language
 RDBMS의 데이터를 관리하기 위해 만들어진 언어

명령
-정의 CREATE DROP ALTER TRUNCATE
-조작 INSERT UPDATE DELETE SELECT
-제어 GRANT REVOKE

data type
-boolean
-character (CHAR, VARCHAR)
-Exact numeric (NUMERIC, DECIMAL, INTERGER, SMALLINT, BIGINT)
-Approximate numeric (REAL, FLOAT, DOUBLE)
-Datetime (DATE, TIME, TIMESTAMP) / Large Object

#### DDL : data definition language
-CREATE : db 생성
 --constraints
	NOT NULL
	UNIQUE
	PRIMARY KEY : NOT NULL and UNIQUE
-DROP : db 삭제
-TRUNCATE : db의 값만 날리고 틀은 남게됨
-ALTER : db의 구조를 바꿀 때 사용, column 추가 삭제 수정 등

#### DML : 데이터 조작어
-INSERT
-SELECT * : ALL, DISTINCT : 중복 제거한 전부
-LIKE find a string fitting a certain description / % wildcard
-UPDATE : where 절을 조심해서 쓰지 않으면 싹 바뀜
-DELETE : 특정 row를 지움
-JOIN : combines columns from one or more tables in a relational database, based on a related column between them
	--INNER JOIN : 교집합
	--LEFT JOIN : 왼쪽 테이블(기준 테이블)의 값 중 오른쪽에서 해당되는 값들을 보여줌
	--RIGHT JOIN
	--OUTER JOIN


### SQLite
무료 오픈 소스 DB
serverless - 파일 형태로 저장
Self-contained
Single Disk File
Zero-configuration
Supports RDBMS Features

```import sqlite3
conn = sqlite3.connect('경로/이름' or ':memory:') - 연결과 관련된 객체
cur = conn.cursor() - db를 다루는 객체
cur.execute('SQL문') - question marks and named placeholder가 가능
executemany - 동일한 SQL문을 반복하기 위한 구문
fetchall() - 버퍼에 담긴 연산 결과를 출력하는 구문
```

2.1 ORM : object relational mapping
 programming technique for converting data between imcompatible type system using objeck-oriented programmming languages

## why use ORM?
- Mismatch between the object model and the relational database
- ORM frees the programmer from dealing with simple repetitive datebase quieris
- Automatically mapping the database to business objects
- Programmers focus more on business problems and less with data storage
- the mapping process can aids

ORMs 중 SQLAlchemy를 쓴다


# 220906
SQLAlchemy - ORM(Mapping! Object-Realational Table)
					->	SQL(DB)
					->	Talbe Object(MetaData Class)
					->	insert, delete (실제 DB 통신 - Lazy)
					->	AND, OR, NOT, ... LIKE => 예제에선 :memory:에 저장했었다.

## 새로 시작시,
1. MetaData Instance 생성
2. Table Instance 생성 후 MetaData에 등록(파라미터로 등록 / 나중에 할 수도 있음)
3. engine Instance 생성
4. engine으로 Tables 물리적 DB에 생성
5. insert()
6. join()
7. select
## 새로 시작하는 경우가 아니라면
1. MetaData.clear(), engine.dispose()
2. 나머지는 위와 동일


### session
import sqlalchemy.orm.session session

### relationship
부모 입장 : 내 자식은 누구누구
자식 입장 : 내 부모는 누구다.
backref : table 간의 부모자식을 중 단방향/한쪽만 설정하는 방법
back_populate : 양방향에 관계를 명시하는 것



Instagram => 본문내용, #해시태그, ...
테이블 -> 클래스 설계
:Create

Post(내용, 태그,태그...)
Post DB -> 내용, 태그 디비 -> 태그1,태그2... => 클래스 함수
내용 ~ 태그들 출력

:Update
Post 내용 수정
Tag 수정(+-1)
