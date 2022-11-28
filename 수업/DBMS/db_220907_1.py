# 220906의 수업 내용 요약
from sqlalchemy import create_engine, MetaData
from sqlalchemy.schema import Table, Column, ForeignKey
from sqlalchemy.sql import select, join

engine = create_engine('sqlite:///playlist.db', echo=True)
meta = MetaData(engine)

artist = Table('T_ARTIST', meta, extend_existing=True, autoload=engine)
album = Table('T_ALBUM', meta, extend_existing=True, autoload=engine)
genre = Table('T_GENRE', meta, extend_existing=True, autoload=engine)
track = Table('T_TRACK', meta, extend_existing=True, autoload=engine)


album.c.AFK.append_foreign_key(ForeignKey(artist.c.PK))

engine.execute(select([album.c.NAME, artist.c.NAME])\
               .select_from(album.join(artist))).fetchall()

meta.clear(), engine.dispose()
#################################################################################
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.types import Integer, Text

engine = create_engine('sqlite:///:memory:', echo=True)
base = declarative_base()

class TableA(base):
    __tablename__ = 'T_A'
    PK = Column('PK', Integer, primary_key=True) #SQList에선 primary key로 설정하면 autoincrement가 자동으로 설정된다
    NAME = Column('NAME', Text)

class TableB(base):
    #테이블 비 보여주세요
    __tablename__ = 'T_B'
    PK = Column('PK', Integer, primary_key=True) #SQList에선 primary key로 설정하면 autoincrement가 자동으로 설정된다
    NAME = Column('NAME', Text)
    FK = Column('FK', Integer, ForeignKey('T_A.PK'), nullable=False)


Session = sessionmaker(engine)
session = Session()

# base.metadata.tables
base.metadata.create_all(engine)

a = TableA(NAME='테스트A')

session.add(a)
session.commit()
session.autocommit = True

b = TableB(NAME='A랑 연관된 B', FK=a.PK)

session.add(b)

session.add(TableA(NAME='두번째 A'))
# session.commit()
a2 = session.query(TableA).all()[-1]
a2.PK
aList = [a, a2]

for _ in aList:
    if _.PK == 1:
        print(_.NAME)


print(session.query(TableA).filter(TableA.PK == 1).one().PK)

for _ in session.query(TableB, TableB.FK, TableA.NAME)\
        .select_from(TableB).join(TableA, TableB.FK==TableA.PK).all():
    print(_.NAME, _.FK)


base.metadata.clear(), engine.dispose()
###############################################################################
from sqlalchemy.orm import relationship

engine = create_engine('sqlite:///:memory:', echo=True)
base = declarative_base()

class TableA(base):
    __tablename__ = 'T_A'
    PK = Column('PK', Integer, primary_key=True) #SQList에선 primary key로 설정하면 autoincrement가 자동으로 설정된다
    NAME = Column('NAME', Text)

    relationship('TableB', back_populates='parent')

class TableB(base):
    #테이블 비 보여주세요
    __tablename__ = 'T_B'
    PK = Column('PK', Integer, primary_key=True) #SQList에선 primary key로 설정하면 autoincrement가 자동으로 설정된다
    NAME = Column('NAME', Text)
    FK = Column('FK', Integer, ForeignKey('T_A.PK'), nullable=False)

    parent = relationship('TableA', back_populates='child')


Session = sessionmaker(engine, autocommit=True)
session = Session()

# session.query(TableA).all()
base.metadata.create_all(engine)

a1 = TableA(NAME='A1')
a1.child.append(TableB(NAME="B3"))
session.begin()


session.add(a1)
# session.dirty, session.is_modified(a1)