import imp

from operator import or_
from secrets import choice
from sqlalchemy import create_engine
from sqlalchemy.schema import MetaData, Table, Column, ForeignKey
from sqlalchemy.types import Integer, Text

meta = MetaData()
Table('T_CITY', meta,
    Column('PK', Integer, primary_key=True, autoincrement=True),
    Column('NAME', Text, nullable=False),
    extend_existing=True)

Table('T_SUPPLIER', meta,
    Column('PK', Integer, primary_key=True, autoincrement=True),
    Column('NAME', Text, nullable=False),
    Column('CFK', Integer, ForeignKey('T_CITY.PK'), nullable=False),
    extend_existing=True)

Table('T_PART', meta,
    Column('PK', Integer, primary_key=True, autoincrement=True),
    Column('NAME', Text, nullable=False),
    extend_existing=True)

Table('T_SELLS', meta,
    Column('SFK', Integer, ForeignKey('T_SUPPLIER.PK')),
    Column('PFK', Integer, ForeignKey('T_PART.PK')),
    Column('PRICE', Integer),
    extend_existing=True)    

engine = create_engine('sqlite:///0906_1.db', echo=True)
meta.bind = engine
meta.create_all()

from sqlalchemy.sql import insert, select, join, update

city = meta.tables['T_CITY']
supplier = meta.tables['T_SUPPLIER']
part = meta.tables['T_PART']
sells = meta.tables['T_SELLS']

engine.execute(city.insert().values(NAME='도시1'))
engine.execute(city.insert(), [{'NAME':'도시2'},
                               {'NAME':'도시3'},
                               {'NAME':'도시4'}])

engine.execute(insert(part), [{'NAME':'부품1'},
                              {'NAME':'부품2'},
                              {'NAME':'부품3'}])

# 특정 테이블의 정보를 받아오기
print(engine.execute(select(city)).fetchall())

from sqlalchemy.sql import and_, or_, not_

print(city.columns.get('PK2'))
print(city.c.PK)
print((city.columns.get('PK') == 1).compile().params)
print(and_(sells.c.SFK == 1, sells.c.PFK == 2))
print(city.columns.get('NAME').like('%1%'))

from random import choice

for _ in range(5):
    engine.execute(
        insert(supplier).values(
            NAME=f'상점{_}',
            CFK=select(city.c.PK).where(
                city.c.NAME.like(f'%{choice(range(1,5))}')
            ).scalar_subquery()
        )
    )

for _ in range(10):
    engine.execute(
        insert(sells).values(
            SFK=select(supplier.c.PK).where(
                supplier.c.NAME.like(f'%{choice(range(1,5))}')
            ).scalar_subquery(),
            PFK=select(part.c.PK).where(
                part.c.NAME.like(f'%{choice(range(1,5))}')
            ).scalar_subquery()
        )
    )

sList = engine.execute(select(supplier)).fetchall()  

engine.execute(update(sells).values(PRICE=10))

# join
join(supplier, city, supplier.c.CFK==city.c.PK)
#이 문장과
supplier.join(city, supplier.c.CFK==city.c.PK)
#이 문장은 같다.

fromCluase = sells.join(part).join(supplier).join(city)
engine.execute(
    select([city.c.NAME, supplier.c.NAME, part.c.NAME, sells.c.PRICE])\
            .select_from(fromCluase)\
            .where(or_(
                not_(sells.c.SFK==None),
                not_(sells.c.PFK==None)
            )
    )\
    .order_by(city.c.PK, supplier.c.PK, part.c.PK)
).fetchall()

# MetaData.clear()
# engine.dispose()