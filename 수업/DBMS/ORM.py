from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.schema import Table, Column, ForeignKey
from sqlalchemy.types import Integer, Text
from sqlalchemy import create_engine

engine = create_engine('sqlite:///:memory:')
base = declarative_base()
Session = sessionmaker(engine)
session = Session()


class Post(base):
    __tablename__ = 'T_POST'
    pk = Column('PK', Integer, primary_key=True)
    content = Column('CONTENT', Text, nullable=False)
    tags = relationship('PostWithTags', back_populates='post', uselist=True)

    def __init__(self, content, *tags):
        self.content = content

        session.add(self)
        session.commit()

        self.appendTags(*tags)

#
    def appendTags(self, *tags):
        for tag in tags:
            q = session.query(Tag).filter(Tag.name.like(f'%{tag}%'))
            if q.count() == 0:
                t = Tag(tag)
                print(f'태그풀에 새로 등록된 태그: {tag}')
            else:
                t = q.first()
                print(f'태그풀에 이미 등록된 태그: {tag}')

            if session.query(PostWithTags).filter(PostWithTags.pfk == self.pk, PostWithTags.tfk == t.pk).count() == 0:
                t.count += 1
                session.add(PostWithTags(pfk=self.pk, tfk=t.pk))
                session.commit()
                print(f'PK:{self.pk} 포스트에 새로 등록된 태그: {tag}')
            else:
                print(f'PK:{self.pk} 포스트에 이미 등록된 태그: {tag}')

    def removeTags(self, *tags):
        for tag in tags:
            q = session.query(Tag).filter(Tag.name.like(f'%{tag}%')).offset(0).limit(1)
            if q.count() > 0:
                t = q.one()
                t.count -= 1

                _t = session.query(PostWithTags).filter(PostWithTags.pfk == self.pk, PostWithTags.tfk == t.pk).offset(
                    0).limit(1)
                if _t.count() > 0:
                    #                     self.tags.remove(_t.one())
                    session.delete(_t.one())
                    session.commit()
                    print(f'PK:{self.pk} 포스트에서 삭제되는 태그: {tag}')
                else:
                    print(f'PK:{self.pk} 포스트에 등록 안된 태그: {tag}')
            else:
                print(f'태그풀에 등록되지 않은 태그: {tag}')

    def getTags(self):
        tags = list()
        for t in self.tags:
            tags.append({'tag': t.tag.name, 'count': t.tag.count})
        return tags


class Tag(base):
    __tablename__ = 'T_TAG'
    pk = Column('PK', Integer, primary_key=True)
    name = Column('NAME', Text, nullable=False)
    count = Column('COUNT', Integer, default=0, nullable=False)
    posts = relationship('PostWithTags', back_populates='tag', uselist=True)

    def __init__(self, name):
        self.name = name

        session.add(self)
        session.commit()


        posts = list()
        for p in self.posts:
            posts.append({'pk': p.post.pk, 'content': p.post.content})
        return posts


class PostWithTags(base):
    __tablename__ = 'T_RELATED'
    dummy = Column('PK', Integer, primary_key=True)
    pfk = Column('PFK', Integer, ForeignKey('T_POST.PK'))
    tfk = Column('TFK', Integer, ForeignKey('T_TAG.PK'))
    post = relationship('Post', back_populates='tags')
    tag = relationship('Tag', back_populates='posts')


base.metadata.create_all(engine)

# 1. 사용자는 콘텐츠를 포스팅할 수 있다.
Post('내용1')

# 2. 포스팅 되는 콘텐츠에는 해시태그가 N개 달릴 수 있다.
Post('내용2', '태그2', '태그3', '태그4')

# for _ in session.query(Post).all():
#     print(_.content, _.getTags())
#
#
# session.query(Post).first().appendTags('태그3', '태그4')
#
# for _ in session.query(Post).all():
#     print(_.content, _.getTags())
#
#
# for _ in session.query(Tag).all():
#     print(_.name, _.getPosts())
#
#
# for _ in session.query(PostWithTags).all():
#     print(_.pfk, _.tfk)
#     print(_.post.pk, _.post.content, _.tag.pk, _.tag.name)


base.registry.dispose(), base.metadata.clear()