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

## Training
https://colab.research.google.com/drive/1VSZF6bSqQn5yGjv3HJEImHuv39n6GQlI?usp=share_link
ipynb 파일 다운로드(colab으로 실행 권장)
colab : https://colab.research.google.com/?hl=ko
ipynb 파일 열어서 구글드라이브와 마운트
/content/drive/MyDrive 에 학습된 모델 업로드(Prerequisites에서 다운 받은 모델)
추가 학습할 데이터셋 /content/drive/MyDrive/Data 에 업로드
/content/drive/MyDrive/Data/images에 모든 학습 이미지 
/content/drive/MyDrive/Data/labels에 모든 학습 라벨
/content/drive/MyDrive/Data/splits에 train과 validation 나누는 기준 txt파일(train.txt, val.txt)

모든 셀 실행

```


```

## Built With

* [mmsegmentation](https://github.com/open-mmlab/mmsegmentation) - open source semantic segmentation toolbox based on PyTorch


