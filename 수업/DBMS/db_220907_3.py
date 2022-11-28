from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import Integer, Text
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.schema import Table, Column, ForeignKey

engine = create_engine('sqlite:///:memory:', echo=True)
base = declarative_base()
Session = sessionmaker(engine)#, autocommit=True)
session = Session()

class Post(base):
    __tablename__ = 'T_POST'
    PK = Column('PK', Integer, primary_key=True)
    CONTENT = Column('CONTENT', Text, nullable=False)
    TAGS = relationship('Tag', back_populates='POST', uselist=True)

    def addTags(*TAGS):
        for _ in TAGS:
            if len(session.query(Tag)).all() > 0:
                session.query(Tag).filter(Tag.name == _).addCount()
            else:
                session.add(Tag(NAME=tag, fk=self.PK))
            session.commit()

class Tag(base):
    __tablename__ = 'T_TAG'
    PK = Column('PK', Integer, primary_key=True)
    NAME = Column('NAME', Text, nullable=False)
    COUNT = Column('COUNT', Integer, default=1)
    FK = Column('FK', Integer, ForeignKey('T_POST.PK'))
    POST = relationship('Post', back_populates='TAGS')

    def addCount(self):
        self.COUNT += 1
        session.commit()


base.metadata.create_all(engine)

post1 = Post(CONTENT="내용1")
session.add(post1)
session.commit()
# 입력이 되었는지 확인하는 부분
print(post1.PK)

tag1 = Tag(NAME='태그1')
# tag1.addCount()
session.add(tag1)
session.commit()
print(tag1.NAME)

print(post1.TAGS)
post1.addTags(tag1.NAME)
# post1.TAGS[-1].addCount()
# post1.TAGS[-1].COUNT

# artist = session.query(Artist).all[0]
# artist.albums.append(Album(Name='앨범4', AFK=artist.PK))


session.dirty
session.is_modified(post1)
session.commit()


