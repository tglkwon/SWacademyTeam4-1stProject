import seaborn as sns
tips = sns.load_dataset('tips')
tips.rename(columns={'tips':'tips2'}, inplace=True)

import numpy as np
a = np.arange(10)
a.reshape(5,-1)
a.reshape(2,-1)
# reshape에 음수를 넣으면 소수곱인 경우 나머지를 자동으로 계산해 넣어준다.
# size는 갯수고 줄어들면 뒷부분을 잘라내고, 늘어나면 zero padding이 일어난다.
a.resize(3,4)
a.resize(3,2, refcheck=False)
# 원래 값을 어딘가게 저장해둔다.

a.reshape(2,5, order='F')
# cthone 의 자료 방식, fortran의 자료 방식

a.strides
a.dtype
a.itemsize

a = np.arange(48).reshape(3,4,4)
a.sum(axis=1)
