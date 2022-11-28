# 221019
# 이제까지 배운 것들
큰 덩이의 데이터셋(코퍼스)를 어떻게 수집할 것인가
    focused crawling
크롤한 데이터셋에서 feature extraction을 어떻게 할 것인가
    NLP techniques - Tokenizing, Stemming, POS
document(training)과 query(testing)을 어떻게 표현할 것인가
    Bag of words - 모든 단어들은 독립적임
    Vector Space Model - 각 단어들이 하나의 차원으로 표현함

# 심볼 정의
f : 학습시키려는 타겟 함수
g : 기계학습의 학습된 함수
g(D) : 데이터셋(D)를 이용해 학습한 학습된 함수
D : 현실 세계에서 가져온 데이터셋
_g : 무한히 많은 수의 데이터셋에서 학습시킨 함수들의 평균, 기댓값

# Bias and Variance from loss function
모델의 복잡도를 높여서 진리값과의 오차를 줄이고
데이터셋의 양을 늘려서 샘플링에 의한 오차를 줄여야 한다.

# 진리값을 모를 때 성능을 측정하는 방법 - Cross Validation, confusion matrix
전체 데이터셋을 가질 수는 없으니 우리가 가진 데이터셋을 전체라고 가정한다.
데이터셋을 N개로 나눠서 1개는 테스트(성능평가)용, N-1개를 학습용으로 쓴다. 그리고 이를 다른 부분으로 반복한다.

# precision and Recall
            Actual
Predicted   Positive    Negative
Positive    True Positive   False Positive
Negative    False Negative  True Negative

Precision TP / (TP+FP)   우리 정답 중에 진짜 정답의 비율 - 스팸 필터링
Recall TP / (TP+FN)     진짜 정답 중에 잘못 판단한 비율 - CRM VIP판별 시스템 -진짜 VIP를 놓친 비율
탐색 범위를 올리면 Recall이 높아지고 precision이 떨어진다

# F-Measure

F1-Measrue = Precision과 Recall을 균등하게 영향을 확인하는 지표