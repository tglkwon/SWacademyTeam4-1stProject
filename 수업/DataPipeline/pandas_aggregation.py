import seaborn as sns
import pandas as pd
import missingno

mpg = sns.load_dataset('mpg')
# mpg.missingno.matrix

# missing data를 채우는 테크닉 impute
# 평균, 중간값, 최빈값 + 추천 알고리즘에서 썼던 비슷한 데이터 값을 찾을 수도 있다.
# mpg[mpg['horsepower'].isna()]

mpg[mpg.origin == 'usa'].horsepower.describe()
mpg.groupby('origin').mean()[['horsepower', 'weight']].plot.bar(stacked=True)
mpg.groupby('origin')[['horsepower', 'weight']].mean()
# 필요한 정보를 계산하는 것도 순서와 방법을 잘 찾아야 한다.

# groupby를 구현하는 개념 - split, imply, combine 카테고리 별 특성을 찾는 방법

temp = mpg.groupby('origin')[['horsepower', 'weight']]
temp.agg(['mean', 'std'])
temp.aggregate(['mean', 'std'])

tips = sns.load_dataset('tips')
tips.groupby(['smoker', 'day'], as_index=False).mean()
# 전반적인 경향성을 미리 확인하기 좋다

# aggregation 분석하는 방법
# margin 전체의 최대
tips.pivot_table(index='sex', columns='smoker', values='tip', aggfunc='max', margins=True)
pd.pivot_table(tips, index='sex', columns='smoker', values='tip', aggfunc='max')
# tips.show()

tips.groupby(['sex', 'smoker']).mean()
tips.groupby(['sex', 'smoker'])['tip'].mean().unstack()

pd.crosstab(tips.sex, tips.smoker, values=tips.tip, aggfunc='mean')
