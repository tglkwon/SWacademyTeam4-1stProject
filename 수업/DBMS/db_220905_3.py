from re import T
import sqlalchemy
engine = sqlalchemy.create_engine('sqlite:///memory.db', echo=True)

from sqlalchemy.schema import MetaData, Table, Column
from sqlalchemy.types import Integer, Text

meta = MetaData(engine)
t_city = Table('T_CITY', meta,
    Column('PK', Integer, primary_key=True),
    Column('NAME', Text))

# meta.tables
meta.create_all()


from sqlalchemy import insert, select

city = meta.tables['T_CITY']
insert(city).values()

engine.execute(insert(city), [{'PK': None, 'NAME': '도시1'},
							{'PK': None, 'NAME': '도시2'},
							{'PK': None, 'NAME': '도시3'}])


from sqlalchemy import ForeignKey

t_supplier = Table('T_SUPPLIER', meta,
	Column('PK', Integer, primary_key=True),
	Column('NAME', Text),
	Column('CITY', Integer, ForeignKey('T_CITY.PK')))

meta.create_all()

engine.dispose()