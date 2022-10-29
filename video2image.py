import cv2

# image로 분리할 파일 이름
fileName = '''collection 5'''
# 파일 위치
cap = cv2.VideoCapture(f'videos/{fileName}.mp4')

width = cap.get(3)
height = cap.get(4)
fps = int(cap.get(cv2.CAP_PROP_FPS))

count = 0
while True:
    ret, fram = cap.read()

    if ret:
        if(int(cap.get(1)) % fps == 0): #앞서 불러온 fps 값을 사용하여 1초마다 추출
            cv2.imwrite(f"videos/X/{fileName}_{count}.jpg", fram)
            print('Saved frame number :', str(int(cap.get(1))))
            # 몇 개마다 추출 할지
            count += 3
    else:
        break

cap.release()
