# DigitalYard

### Prerequisites

학습된 semantic segmentation 모델 다운로드

https://drive.google.com/file/d/1ALL7M4HhXtudpXTEz28IknEMv-CCn_rq/view?usp=sharing

다운로드 된 파일을 DigitalYard 폴더에 추가(ImageViewer.py와 같은 경로)


### Installing
파이썬 3.8 권장
```
pip install -r requirements.txt
pip install torch==1.11.0 torchvision --extra-index-url https://download.pytorch.org/whl/cu113
mim install mmcv-full==1.5.3
```


## Running

```
python ImageViewer.py

```
ImageViewer 기능
- 이미지 담긴 폴더 선택하여 맵 생성(ctrl+o)
- 맵 확대 및 축소(ctrl++, ctrl+-)
- 맵 창크기에 맞춤
- 맵 원본 크기로 보기
- 맵 위에 각 레이어(블럭, 도로, 건물) 표시
- 두 포인트 클릭으로 두 포인트간 거리 계산
- shift+마우스 클릭 후 드래그로 사각형 내의 넓이 계산
- 맵 저장

## DataSet
데이터셋 제작툴 : cvat

cvat 웹페이지로 사용 가능하나 서버가 자주 다운되는 관계로 docker로 local에서 실행 권장

cvat docker 사용법: https://smart-factory-lee-joon-ho.tistory.com/203

cvat에서 라벨링할 이미지셋을 업로드 후 polygon 형식으로 annotation 작업 진행

annotation 예시: ![image](https://user-images.githubusercontent.com/74086927/204449809-7b6cae9f-8d42-4566-a21c-f4b6346366bf.png)

annotation 작업 후 cityscapes 형식으로 데이터셋 내보내기

다운된 zip 파일 압축 후 /gtFine/default에 있는 라벨들 중 labelIds 파일들 제외하고 다 삭제

## Training
https://colab.research.google.com/drive/1VSZF6bSqQn5yGjv3HJEImHuv39n6GQlI?usp=share_link

ipynb 파일 다운로드(colab으로 실행 권장)

colab : https://colab.research.google.com/?hl=ko

ipynb 파일 열어서 구글드라이브와 마운트

/content/drive/MyDrive 에 학습된 모델 업로드(Prerequisites에서 다운 받은 모델)
추가 학습할 데이터셋 /content/drive/MyDrive/Data 에 업로드
/content/drive/MyDrive/Data/images에 모든 학습 이미지 업로드
/content/drive/MyDrive/Data/labels에 모든 학습 라벨 업로드(라벨 파일의 이름을 이미지 파일의 이름과 같게 수정;맨뒤 labelIds )
/content/drive/MyDrive/Data/splits에 train과 validation 나누는 기준 txt파일(train.txt, val.txt, 보통 8:2로 나눔)

train과 validation은 랜덤 선택하여 8:2로 나눠야 함
train.txt 예시: [train.txt](https://github.com/smc2315/DigitalYard/files/10110165/train.txt)

모든 셀 실행

```


```

## Built With

* [mmsegmentation](https://github.com/open-mmlab/mmsegmentation) - open source semantic segmentation toolbox based on PyTorch


