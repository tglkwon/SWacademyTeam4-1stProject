import pandas as pd

data = pd.read_csv(".\data\pew.txt", sep='\t')
pew = data.set_index('religion').stack().reset_index()

# 관계형 DB을 join한 것처럼 정리되어 있는 데이터를 원 DB형 데이터로 돌리는 방법
data.melt('religion', var_name='earns', value_name='cnt')

# billboard = pd.read_csv('https://github.com/hadley/tidy-data/blob/master/data/billboard.csv', encoding='latin1')
billboard = pd.read_csv('./data/billboard.csv', encoding='latin1')
# moltenBillboard = billboard.melt(['year', 'artist.inverted', 'track', 'time', 'genre', 'date.entered', 'date.peaked'])

moltenBillboard = billboard.melt(billboard.columns[:7]).dropna().reset_index(drop=True)
moltenBillboard.value = moltenBillboard.value.astype('uint8')

for i in moltenBillboard.itertuples():
    print(i)
    break


# named tuple : dict처럼 key value같이 value별 name이 있다.
from collections import namedtuple
Point = namedtuple('Point', ['x','y'])
p1 = Point(x=3, y=4)
p1.x == p1[0]

# map series에서만 쓸 수 있다.
weeks = moltenBillboard.variable.map(lambda x:x[:-7]).map(lambda x:x[1:]).astype('int')

import re
# weeks = moltenBillboard.variale.map(lambda x: re.search(r'(\d+)', x)).astype('int')

# pandas 에서 map
import seaborn as sns
tips = sns.load_dataset('tips')

tips.sex.map(lambda x: x[0])
tips.sex.apply(lambda x: x[0])
tips.sex.map({'Female': 'F', 'Male': 'M'})

# apply는 series / dataframe 둘 다 사용 가능하다
tips.apply(lambda x: x['total_bill'] + x['tip'], axis=1)
tips.select_dtypes('number').apply(lambda x: x+1, axis=0)
# 모든 셀 별로 계산하는 방법
tips.select_dtypes('number').applymap(lambda x:x+1)

moltenBillboard.variable.str.extract('(\d+)', expand=False)
moltenBillboard.variable.str[1:].str[:-7]

data = pd.read_csv('https://raw.githubusercontent.com/hadley/tidy-data/master/data/tb.csv', encoding='latin1')
tb = data.melt(['iso2', 'year']).dropna()
tb.variable.value_counts()
# tb.variable.str.contains('_f')
tb['sex'] = tb.variable.map(lambda x: 'F' if '_f' in x else 'M' if '_m' in x else '?')

# tips['size'].astype('category')
# ML에서 문자를 숫자로 처리하는 기법과 비슷, 연동 가능
tips['sex'].cat.codes
tips['sex'].cat.categories

# DB 쿼리 형식으로 다룰 수도 있다.
# tips.query()

mpg = sns.load_dataset('mpg')
mpg.name.value_counts()
mpg.name.str.split(' ', expand=True)[0].value_counts()