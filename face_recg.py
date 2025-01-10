import face_recognition
import cv2
import numpy as np
import dlib

# 加载已知人脸图像
known_name = "zyx"
path = "known_people/" + known_name + ".jpg"
known_image = face_recognition.load_image_file(path)
known_encoding = face_recognition.face_encodings(known_image)[0]

# 加载 dlib 的预训练模型
face_detector = dlib.get_frontal_face_detector()

# 加载 5 点特征点模型
shape_predictor = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")  # 确保文件路径正确

# 加载人脸编码模型
face_encoder = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

# 初始化摄像头
video_capture = cv2.VideoCapture(0)

while True:
    # 捕获视频帧
    ret, frame = video_capture.read()

    if ret:
        # 将帧转换为 RGB 格式
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # 检测人脸
        face_locations = face_recognition.face_locations(rgb_frame)
        print(type(face_locations))
        print("Found {} faces in image.".format(len(face_locations)))

        if len(face_locations) > 0:
            # 计算人脸编码
            face_encodings = face_recognition.face_encodings(
                rgb_frame,
                known_face_locations=face_locations,
                model="small"  # 使用 "small" 模型（5 点特征点模型）
            )

            for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
                # 对比已知人脸
                matches = face_recognition.compare_faces([known_encoding], face_encoding)
                name = "Unknown"

                if matches[0]:
                    name = known_name

                # 绘制人脸框和标签
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 0, 0), 2)

        # 显示结果
        cv2.imshow('Video', frame)

    # 按 'q' 退出
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头并关闭窗口
video_capture.release()
cv2.destroyAllWindows()