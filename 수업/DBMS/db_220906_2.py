from sqlalchemy.sql import insert, select, join, update
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData, Table, Column, ForeignKey
from sqlalchemy.types import Integer, Text

engine = create_engine('sqlite:///playlist.db', echo=True)
meta = MetaData(engine)

Table('T_ARTIST', meta, autoload=engine)
Table('T_ALBUM', meta, autoload=engine)
Table('T_GENRE', meta, autoload=engine)
Table('T_TRACK', meta, autoload=engine)

len(meta.tables)

print(engine.execute(meta.tables['T_ARTIST'].select()).fetchall())

artist = meta.tables['T_ARTIST']
album = meta.tables['T_ALBUM']
genre = meta.tables['T_GENRE']
track = meta.tables['T_TRACK']

print(engine.execute(
    select([artist.c.NAME, album.c.NAME, genre.c.NAME, track.c.NAME])\
    .select_from(
        join(artist, album, artist.c.PK==album.c.AFK).\
        join(track, track.c.AFK==album.c.PK).
        join(genre, track.c.GFK==genre.c.PK)
    )\
    .where(track.c.COUNT > 5)
    .order_by(artist.c.PK, album.c.PK, track.c.NAME)
).fetchall())


engine.dispose()
meta.clear()

engine = create_engine('sqlite:///:memory:', echo=True)
from sqlalchemy.ext.declarative import declarative_base
base = declarative_base()
base.metadata.tables
base.metadata.create_all(engine)

user1 = User(NAME='test')

from sqlalchemy.orm.session import sessionmaker

Session = sessionmaker(engine)
session = Session()
session.add(user1)
session.is_modified(user1)

session.commit()
session.close()
