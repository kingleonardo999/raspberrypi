# 树莓派智能小车

## 前言

本项目是基于树莓派5实现的智能小车，项目来源于学校课程，发布到GitHub上便于交流学习

## 功能实现

1.   基本的运动，前进、后退、左右旋转等
2.   使用`USB`摄像头进行拍照、摄像
3.   基于本地下载的模型 `deploy.prototxt` 和 `res10_300x300_ssd_iter_140000.caffemodel` 的人脸检测
4.   基于`opencv`的人脸检测，以及人脸识别
5.   基于`insightface`实现的人脸识别和人脸追踪
6.   基于`dlib`和`face_recognition`实现的人脸识别

### 使用要点

1.   使用`jupyter`运行.ipynb文件
2.   人脸识别部分需要添加人脸数据，首次使用需添加`known_people`文件夹，并放入人像图片
3.   运行`insightface_face_id.ipynb`时，首次运行或者人脸变更需要先运行`load_imgs.ipynb`

