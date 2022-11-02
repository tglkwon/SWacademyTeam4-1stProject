from pytube import YouTube, Playlist
import cv2
import os
from PIL import Image

#---------------------------------------------------------#
### video download from youtube playlist

# 저장 폴더
DOWNLOAD_FOLDER = " "

# 가져올 유튜브 재생목록 링크
p = Playlist(" ")
for video in p.videos:
    video.streams.filter(file_extension="mp4").first().download(DOWNLOAD_FOLDER)
    print("다운로드 완료")


#---------------------------------------------------------#
### image capture from video files

# 처리할 동영상 폴더 경로
file_path = " "

# 추출한 이미지 저장할 폴더 생성
try:      
    if not os.path.exists('imageset'):
        os.makedirs('imageset')

except OSError:
    print ('Error: Creating directory of data')

# 동영상에서 이미지 추출    
video_names = os.listdir(file_path)
for video_name in video_names:
    cap = os.path.join(file_path, video_name)
    cam = cv2.VideoCapture(cap)
  
    currentframe = 0

    while True:   
        # 프레임 읽기
        ret,frame = cam.read()
        if ret:
            # 125 프레임마다 이미지 추출
            if (currentframe % 125) == 1:
                name = './imageset/' + video_name + 'frame' + str(currentframe) + '.jpg'
                print ('Creating...' + name)

                # 이미지 저장
                cv2.imwrite(name, frame)

                # 프레임 카운트
                currentframe += 1
            else:
                currentframe += 1     
        else:
            break

    # 캡쳐 윈도우 종료
    cam.release()
    cv2.destroyAllWindows()


#---------------------------------------------------------#
### image file name change

# 추출한 이미지 폴더 경로
file_path = " "

# 폴더 내 이미지 이름들
file_names = os.listdir(file_path)
# print(file_path)
# print(file_names)

# 오름차순으로 이미지 이름 일괄 변경
num = 1 
for name in file_names:
    src = os.path.join(file_path, name)
    dst = str(num) + '.jpg'
    dst = os.path.join(file_path, dst)
    os.rename(src, dst)
    num += 1


#---------------------------------------------------------#
### image file resize and crop

# 추출한 이미지 폴더 경로
file_path = " "

# 크롭한 이미지 저장할 폴더 생성
try:      
    if not os.path.exists('/Users/jongseopark/Desktop/INISW_Academy/team_project/1st_project/data/classic_popeye_videoset/imageset/cropped'):
        os.makedirs('/Users/jongseopark/Desktop/INISW_Academy/team_project/1st_project/data/classic_popeye_videoset/imageset/cropped')

except OSError:
    print ('Error: Creating directory of data')
    
# 이미지 리사이즈 및 크롭
for i in range (14100):
    filename = str(i) + '.jpg'
    if filename in os.listdir(file_path):
        try:
            image_name = os.path.join(file_path, filename)
            image = Image.open(image_name)
            # print(image_name)

            newsize = (460, 256)
            image = image.resize(newsize)

            croppedImage=image.crop((102,0,358,256))

            save_path = os.path.join(file_path, 'cropped/', str(i))
            croppedImage.save(save_path + '_cropped.jpg')
        except:
            print(str(i) + '-no filename')
            continue