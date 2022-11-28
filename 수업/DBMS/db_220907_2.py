from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Text
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.schema import Table, Column, ForeignKey

engine = create_engine('sqlite:///playlist.db', echo=True)
base = declarative_base()
meta = MetaData(engine)

Table('T_ARTIST', meta, extend_existing=True, autoload=engine)
Table('T_ALBUM', meta, extend_existing=True, autoload=engine)
Table('T_GENRE', meta, extend_existing=True, autoload=engine)
Table('T_TRACK', meta, extend_existing=True, autoload=engine)

afk = base.metadata.album.c.AFK
afk.append_foreign_key(ForeignKey(base.metadata.tables['T_ARTIST'].c.PK))

# engine.execute(.)

class Artist(base):
    __tablename__ = base.metadata.tables['T_ARTIST']
    # PK = Column('PK', Integer, primary_key=True) #SQList에선 primary key로 설정하면 autoincrement가 자동으로 설정된다
    # NAME = Column('NAME', Text)

    albums = relationship('Album', back_populates='artist', uselist=True)
    def addAlbum(self, name):
        self.albums.append(Album(NAME=name, AFK=self.PK))

class Album(base):
    #테이블 비 보여주세요
    __tablename__ = base.metadata.tables['T_ALBUM']
    # PK = Column('PK', Integer, primary_key=True) #SQList에선 primary key로 설정하면 autoincrement가 자동으로 설정된다
    # NAME = Column('NAME', Text)
    # FK = Column('FK', Integer, ForeignKey('T_A.PK'), nullable=False)

    artist = relationship('Artist', back_populates='albums')


Session = sessionmaker(engine, autocommit=True)
session = Session()

# session.query(TableA).all()
base.metadata.create_all(engine)

# session.begin()

# print(join(base.metadata.tables['T_ALBUM'], base.metadata.tables['T_ARTIST']))
# engine.execute(select(base.metadata.tables['T_ALBUM'])\
#                .select_from(
#                     join(base.metadata.tables['T_ARTIST'])
# ))

artist = session.query(Artist).all[0]

artist.albums.append(Album(Name='앨범4', AFK=artist.PK))

session.add(artist)
session.commit()