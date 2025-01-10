import os
import cv2
import numpy as np
import pickle

current_id = 0
label_ids = {}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
image_dir = os.path.join(BASE_DIR, "dataset")
x_train = []
y_labels = []

recognizer = cv2.face.LBPHFaceRecognizer_create()
# 加载分类器
classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

for root, dirs, files in os.walk(image_dir):
    for file in files:
        # 只处理jpg和png文件
        if file.endswith("jpg") or file.endswith("png"):
            # 绝对路径
            path = os.path.join(root, file)
            # 读取图片
            image = cv2.imread(path)
            # 转成灰度图
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # 转成numpy数组
            image_array = np.array(gray, "uint8")
            label = os.path.basename(root)
            # 添加对应关系的id，如果没有添加过，就添加
            if not label in label_ids:
                label_ids[label] = current_id
                current_id += 1

            id_ = label_ids[label]

            # 检测人脸
            faces = classifier.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=5)

            for (x, y, w, h) in faces:
                # 获取人脸区域
                roi = image_array[y:y+h, x:x+w]
                # 添加到训练集
                x_train.append(roi)
                y_labels.append(id_)

# 保存对应关系
with open("labels.pickle", "wb") as f:
    pickle.dump(label_ids, f)

recognizer.train(x_train, np.array(y_labels))
# 保存训练结果
recognizer.save("trainner.yml")