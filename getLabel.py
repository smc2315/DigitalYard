import os

from mmsegmentation.mmseg.apis import inference_segmentor, init_segmentor
import mmcv


import numpy as np

from mmcv import Config

#config 로드 및 설정
config_file = os.path.join(os.path.dirname(__file__), 'utils/segformer_mit-b5_8x1_1024x1024_160k_cityscapes.py')
cfg = Config.fromfile(config_file)
cfg.norm_cfg = dict(type='BN', requires_grad=True)
cfg.model.decode_head.norm_cfg = cfg.norm_cfg
cfg.model.decode_head.num_classes = 4
cfg.img_norm_cfg = dict(
    mean=[123.675, 116.28, 103.53], std=[58.395, 57.12, 57.375], to_rgb=True)
cfg.crop_size = (507, 760)
cfg.train_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(type='LoadAnnotations'),
    dict(type='Resize', img_scale=(1014, 760), ratio_range=(0.5, 2.0)),
    dict(type='RandomCrop', crop_size=cfg.crop_size, cat_max_ratio=0.75),
    dict(type='RandomFlip', flip_ratio=0.5),
    dict(type='PhotoMetricDistortion'),
    dict(type='Normalize', **cfg.img_norm_cfg),
    dict(type='Pad', size=cfg.crop_size, pad_val=0, seg_pad_val=255),
    dict(type='DefaultFormatBundle'),
    dict(type='Collect', keys=['img', 'gt_semantic_seg']),
]

cfg.test_pipeline = [
    dict(type='LoadImageFromFile'),
    dict(
        type='MultiScaleFlipAug',
        img_scale=(1014, 760),
        # img_ratios=[0.5, 0.75, 1.0, 1.25, 1.5, 1.75],
        flip=False,
        transforms=[
            dict(type='Resize', keep_ratio=True),
            dict(type='RandomFlip'),
            dict(type='Normalize', **cfg.img_norm_cfg),
            dict(type='ImageToTensor', keys=['img']),
            dict(type='Collect', keys=['img']),
        ])
]


#segementation 모델 로드
checkpoint_file = os.path.join(os.path.dirname(__file__), 'iter_4000.pth')
model_ckpt = init_segmentor(cfg, checkpoint_file,device='cuda:0')  #cuda gpu 사용

# 모델로 라벨 얻기
# 이때 얻어진 라벨은 2차원(높이x너비, 각 원소는 해당 위치 픽셀이 속하는 클래스를 의미)
def getLabel(path):

    img = mmcv.imread(path)
    result = inference_segmentor(model_ckpt, img)
    return result

#라벨들 3차원으로 바꾸고 분리(블럭,도로,건물) 및 색 지정
def getLayer(result):
    seg = result
    palette1 = [[0, 0, 0], [51, 221, 255], [0, 0, 0], [0, 0, 0]] # 블럭
    palette2 = [[0, 0, 0], [0, 0, 0], [102, 255, 102], [0, 0, 0]] # 도로
    palette3 = [[0, 0, 0], [0, 0, 0], [0, 0, 0], [250, 250, 55]] # 건물
    palette1 = np.array(palette1)
    palette2 = np.array(palette2)
    palette3 = np.array(palette3)

    color_seg1 = np.zeros((seg.shape[0], seg.shape[1], 3), dtype=np.uint8) #블럭
    color_seg2 = np.zeros((seg.shape[0], seg.shape[1], 3), dtype=np.uint8) #도로
    color_seg3 = np.zeros((seg.shape[0], seg.shape[1], 3), dtype=np.uint8) #건물
    for label, color in enumerate(palette1):
        color_seg1[seg==label, :] = color
    for label, color in enumerate(palette2):
        color_seg2[seg==label, :] = color
    for label, color in enumerate(palette3):
        color_seg3[seg==label, :] = color
    # convert to BGR
    color_seg1 = color_seg1[..., ::-1]
    color_seg2 = color_seg2[..., ::-1]
    color_seg3 = color_seg3[..., ::-1]

    return color_seg1,color_seg2,color_seg3

import cv2
# 이미지 위에 반투명 라벨 표시
def getLayeredImg(img, label):
    img = img.copy()
    h, w = label.shape[:2]
    shapes = np.zeros_like(img, np.uint8)
    shapes[img.shape[0] - h:, img.shape[1] - w:] = label
    mask = shapes.astype(bool)
    img[mask] = cv2.addWeighted(img, 0.5,shapes,0.5,0)[mask]
    return img