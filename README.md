# DigitalYard

### Prerequisites

학습된 semantic segmentation 모델 다운로드

https://drive.google.com/file/d/1ALL7M4HhXtudpXTEz28IknEMv-CCn_rq/view?usp=sharing

다운로드 된 파일을 DigitalYard 폴더에 추가(ImageViewer.py와 같은 경로)


### Installing

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

## Built With

* [mmsegmentation](https://github.com/open-mmlab/mmsegmentation) - open source semantic segmentation toolbox based on PyTorch


