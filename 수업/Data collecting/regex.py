import re
# re.compile() # RE 표현식 만들어주는 함수
# re.escape() # escape 문자(\) => escape 처리해주는 기능
# re.match() # 시작점부터 검사 => ^
# re.search() # 중간에라도 있으면 찾음
# re.split() # 분리
# re.sub() # 찾아서 바꾸기
# re.findall() # 표현식에 맞는 모든 경우 찾기

result = re.search('((?:(sm)|f|(ht))tps?)',
                   'smtp ftp http https')

re.search('h.+s', 'https https https') # => Greedy
re.search('h.+?s', 'https https https') # => Lazy

#regex class

re.search('\d+', '019 2a308 245')
re.search('\s', '019 2a308245')
re.search(r'\b\w+', '019 2a308 245')

userdata = '''
    김씨 941202-1345765
    이씨 000111-4312435
'''

for _ in userdata.splitlines():
    if len(_) > 0:
        result = re.search(r'\b(.+?)\b\s\b(.+?)\b-\b(.+?)\b', _)
        print(f'{result[1]} : {result[2]}-{result[3]}')


# result[0]에는 그룹 전체가 텍스트로 들어가있다

# 전화번호, 주소 => 개인정보라 함부로 수정하면 안된다
# URL, 이메일 => 을 원하는 대로 분리하고 값을 다루기

data = '''
    010-1234-1234
    011-1234-1234
    017-1234-1234
    018-1234-1234
    019-1234-1234
    010-234-1234
    02-1234-1234
    032-234-1234
    019-234-1234
    010-1234-1234   
'''

result = re.findall(r'0[1-9][01789]?\-[0-9]{3,4}\-[0-9]{4}]', data)
# print(result)

# url
data = '''
    http://www.naver.com
    https://www.naver.com
    http://www.daum.net
    https://search.google.co.kr
    naver.com
    https://www.naver.com/path
    https://www.naver.com/path/path.ext
'''

result = re.findall(r'(https?)://(\w+).(\w+.(?:\.\w{2,3}){1,2})((?:/[\w.]+)+)?', data)
# print(result)

# email ID = 소문자 시작, 소문자,숫자,-,_ 로 구성, 6~14자
data = '''
    test1234@naver.com
    test-123@hanmail.net
    tEsT_1t2e@gmail.co.kr
    tesg+dev1@dev-tools.org
    
    Test1234@naver.com
    1test1235@daum.net
'''
# [a-zA-Z\-\_\+]
result = re.findall(r'\b([a-z][A-Za-z0-9\-\_\+]{5,13})@(\w+(?:.\w+)+)\b', data)
print(result)

# 21년 카카오 코딩 테스트
#아이디 3~15자, 소문자, 숫자, -, _, .만 가능, .는 처음과 끝에 사용 불가 및 연속 사용 불가
# 아이디어 정리 : 아이디의 끝이 숫자면 +1

data = '''
    user1id
    .user2id
    userid3.
    .user5id.
    user1.id
    user1-i.d
    userid123456789999
    user1......id
'''
#12 두 글자는 아직 처리 못함
for _ in data.splitlines():
    if len(_) > 0:
        temp = re.sub('[.]{2,}', '..', _.strip())
        temp = re.sub('^[.]', '', temp)
        temp = re.sub('[.]$', '', temp)
        temp = re.search('[a-z0-9\-\_\.]{3,15}', temp).group(0)

        if re.search(r'^[a-z0-9\-_][a-z0-9\-_.]{1,13}[a-z0-9\-_]$', temp) is not None:
            print(_.strip(), '->', temp)



result = re.findall(r'\b([a-z0-9\-\_][a-z0-9\-\_\.]{1,13}[a-z0-9\-\_])@\b', data)
# print(result)


# 2018 카카오 1차 다트 게임
scores = '''
    1S2D*3T
    1D2S#10S
    1D2S0T
    1S*2T*3S
    1D#2S*3S
    1T2D3D#
    10D2S3T*
'''
answers = []
for _ in scores.splitlines():
    answer = 0

    if len(_) > 0:
        points = re.findall(r'(\d{1,2}[SDT][*#]?)', _.strip())

        for _ in points:
            score = re.search(r'(\d{1,2})([SDT])([*#]?)', _)
            # print(score.group())
            point = 0
            if score.group(3) == '#':
                if score.group(2) == 'T':
                    point -= int(score.group(1)) ** 3
                elif score.group(2) == 'D':
                    point -= int(score.group(1)) ** 2
                else:
                    point -= int(score.group(1))
            elif score.group(3) == '*':
                if score.group(2) == 'T':
                    point = point * 2
                    point += int(score.group(1)) ** 3
                elif score.group(2) == 'D':
                    point = point * 2
                    point += int(score.group(1)) ** 2
                else:
                    point = point * 2
                    point += int(score.group(1))
            else:
                if score.group(2) == 'T':
                    point += int(score.group(1)) ** 3
                elif score.group(2) == 'D':
                    point += int(score.group(1)) ** 2
                else:
                    point += int(score.group(1))

            answer += point

        answers.append(answer)


print(answers)