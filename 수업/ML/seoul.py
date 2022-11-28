import pandas as pd

seoul = pd.read_csv('./data/seoul.csv')

food = seoul[seoul[['상권업종소분류코드']]['상권업종소분류코드'].str.startswith('Q')]

fastfood = food[food[['상권업종소분류코드']]['상권업종소분류코드'].str.startswith('Q07')]


market = seoul[seoul['표준산업분류코드'].isna()]
market2 = market[market['상권업종대분류코드'] == 'F']


pd.crosstab(index=market2['상권업종중분류명'], columns=market2['상권업종소분류명'])
