import os
import pickle
import numpy as np
import cv2
import threading
from collections import deque
from insightface.app import FaceAnalysis
from scipy.spatial.distance import cosine

class Camera:
    def __init__(self, src=0, queue_size=10):
        self.cap = cv2.VideoCapture(src)  # 打开摄像头
        if not self.cap.isOpened():
            raise ValueError("无法打开摄像头，请检查摄像头索引或连接")
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
        self.cap.set(cv2.CAP_PROP_FPS, 30)  # 设置帧率为30 fps
        self.FPS = self.cap.get(cv2.CAP_PROP_FPS)  # 获取帧率
        self.thread = None  # 初始化线程属性
        self.queue = deque(maxlen=queue_size)  # 初始化帧队列
        self.processed_queue = deque(maxlen=queue_size)  # 初始化处理后的帧队列
        self.Processed = False  # 默认设置为False
        self.stopped = False
        self.known_face_encodings = []  # 已知人脸编码列表
        self.known_face_names = []  # 已知人脸名字列表
        threading.Thread(target=self.__load_known_faces).start()  # 异步加载已知人脸信息
        # self.__load_known_faces()  # 加载已知的人脸编码和名字

        # 初始化 InsightFace 应用
        self.face_app = FaceAnalysis(providers=['CPUExecutionProvider'])
        self.face_app.prepare(ctx_id=0, det_size=(320, 320))

        self.start()  # 启动摄像头捕获线程

    def __load_known_faces(self):
        """
        加载已知人脸编码和名字文件
        """
        current_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在的目录
        face_features_dir = os.path.join(os.path.dirname(current_dir), 'face_features')  # 构建 face_features 目录的绝对路径

        encodings_file_path = os.path.join(face_features_dir, 'known_face_encodings.pkl')
        names_file_path = os.path.join(face_features_dir, 'known_face_names.pkl')

        if os.path.exists(encodings_file_path) and os.path.exists(names_file_path):
            with open(encodings_file_path, 'rb') as f:
                self.known_face_encodings = pickle.load(f)
            with open(names_file_path, 'rb') as f:
                self.known_face_names = pickle.load(f)
            print(f"已加载 {len(self.known_face_encodings)} 张已知人脸信息")
        else:
            print("警告：未能找到已知人脸信息文件")
            self.known_face_encodings = []
            self.known_face_names = []

    def __load_new_faces(self):
        """
        加载新的已知人脸信息并更新文件
        """
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本所在的目录
            known_people_dir = os.path.join(os.path.dirname(current_dir), 'known_people')  # 构建 known_people 目录的绝对路径
            face_features_dir = os.path.join(os.path.dirname(current_dir), 'face_features')  # 构建 face_features 目录的绝对路径

            # 初始化 InsightFace 应用以提取人脸特征
            app = FaceAnalysis(providers=['CPUExecutionProvider'])
            app.prepare(ctx_id=0, det_size=(320, 320))  # 设置较低分辨率以加快处理速度

            def extract_face_features(image_path):
                img = cv2.imread(image_path)
                faces = app.get(img)
                if faces:
                    return faces[0].embedding
                return None

            def save_embeddings_to_file(embeddings, names, output_folder):
                if not os.path.exists(output_folder):
                    os.makedirs(output_folder)

                encodings_file_path = os.path.join(output_folder, "known_face_encodings.pkl")
                names_file_path = os.path.join(output_folder, "known_face_names.pkl")

                with open(encodings_file_path, 'wb') as f:
                    pickle.dump(embeddings, f)
                with open(names_file_path, 'wb') as f:
                    pickle.dump(names, f)

            for filename in os.listdir(known_people_dir):
                if filename.endswith(".jpg") or filename.endswith(".png"):
                    img_path = os.path.join(known_people_dir, filename)
                    embedding = extract_face_features(img_path)
                    if embedding is not None:
                        self.known_face_encodings.append(embedding)
                        self.known_face_names.append(filename.split('.')[0])  # 假设文件名是人名

            save_embeddings_to_file(self.known_face_encodings, self.known_face_names, face_features_dir)
            self.__load_known_faces()
            print(f"已更新 {len(self.known_face_encodings)} 张人脸信息到 {face_features_dir}")

        except Exception as e:
            print(f"更新人脸信息文件时发生错误: {e}")

    def start(self):
        """
        启动摄像头捕获线程
        """
        if not self.thread:  # 只有当线程未启动时才启动新线程
            self.thread = threading.Thread(target=self.update, args=())
            self.thread.daemon = True  # 设置为守护线程
            self.thread.start()

    def update(self):
        """
        持续从摄像头读取帧并加入队列
        """
        while not self.stopped:
            ret, frame = self.cap.read()
            # print("ret", ret)
            if ret:
                self.queue.append(frame)
            else:
                print("无法抓取帧")
                break

    def read(self):
        """
        根据 self.Processed 的值选择返回原始帧或处理后的帧。
        如果 self.Processed 为 True，则返回 processed_queue 中的内容；
        否则，返回 queue 中的内容。
        如果队列为空，则返回 None。
        """
        target_queue = self.processed_queue if self.Processed else self.queue

        if target_queue:
            frame = target_queue.popleft()
            if frame is None:
                return None
            return bytes(cv2.imencode('.jpg', frame)[1])
        else:
            return None

    def face_detect(self, Mode=0, Specific=False, NewFace=False):
        """
        人脸检测和识别方法

        参数：
        Mode - 模式选择，0为仅检测人脸，1为识别所有人脸，2为识别特定人脸
        Specific - 是否识别特定人脸，默认False
        NewFace - 当开启特定人脸识别时，是否从已知文件中加载人脸并更新人脸信息文件，默认False
        """
        self.Processed = True  # 设置为 True，以便返回处理后的帧
        import time
        time.sleep(0.1)  # 等待队列填充
        if Mode == 0:
            threading.Thread(target=self.__detect_faces).start()
        elif Mode == 1:
            threading.Thread(target=self.__recognize_all_faces).start()
        elif Mode == 2 and Specific:
            if NewFace:
                threading.Thread(target=self.__load_new_faces).start()
            threading.Thread(target=self.__recognize_specific_faces).start()
        else:
            print("无效的模式或参数组合")

    def __detect_faces(self):
        """
        检测人脸并在帧上绘制矩形框
        """
        # i = 0
        # faces = []
        # while not self.stopped:
        #     frame = self.queue.popleft()
        #     if frame is None:
        #         print("没有可用的帧")
        #     if i % 5 < 4:
        #         i += 1
        #     else:
        #         i = 0
        #         faces = self.face_app.get(frame)
        #         print(f"检测到 {len(faces)} 张人脸")
        #     self.__draw_rectangles(frame.copy(), [{'bbox': face.bbox.astype(int), 'name':""} for face in faces])
        while not self.stopped:
            if len(self.queue) == 0:
                continue
            frame = self.queue.popleft()
            if frame is None:
                print("没有可用的帧")

            faces = self.face_app.get(frame)
            print(f"检测到 {len(faces)} 张人脸")
            self.__draw_rectangles(frame.copy(), [{'bbox': face.bbox.astype(int), 'name':""} for face in faces])

    def __recognize_all_faces(self):
        """
        识别所有人脸并在帧上绘制矩形框和标签
        """
        while not self.stopped:
            frame = self.queue.popleft()
            if frame is None:
                print("没有可用的帧")

            faces = self.face_app.get(frame)
            matched_faces = []

            for face in faces:
                embedding = face.embedding
                name = "Unknown"

                # 计算与已知人脸的相似度
                similarities = [1 - cosine(embedding, known_face) for known_face in self.known_face_encodings]
                if similarities:
                    best_match_index = np.argmax(similarities)
                    if similarities[best_match_index] > 0.6:  # 设置相似度阈值
                        name = self.known_face_names[best_match_index]

                matched_faces.append({
                    'bbox': face.bbox.astype(int),
                    'name': name
                })

            print(f"识别到 {len(matched_faces)} 张人脸")
            self.__draw_rectangles(frame.copy(), matched_faces)


    def __recognize_specific_faces(self):
        """
        识别特定人脸并在帧上绘制矩形框和标签
        """
        while not self.stopped:
            frame = self.queue.popleft()
            if frame is None:
                print("没有可用的帧")

            faces = self.face_app.get(frame)
            matched_faces = []

            for face in faces:
                embedding = face.embedding
                name = "Unknown"

                # 计算与特定已知人脸的相似度
                similarities = [1 - cosine(embedding, known_face) for known_face in self.known_face_encodings]
                if similarities:
                    best_match_index = np.argmax(similarities)
                    if similarities[best_match_index] > 0.6:  # 设置相似度阈值
                        name = self.known_face_names[best_match_index]

                matched_faces.append({
                    'bbox': face.bbox.astype(int),
                    'name': name
                })

            print(f"识别到 {len(matched_faces)} 张特定人脸")
            self.__draw_rectangles(frame.copy(), matched_faces)

    def __draw_rectangles(self, frame, matched_faces):
        """
        在给定帧上根据匹配到的人脸信息绘制矩形框和标签，并将结果帧加入到 processed_queue 中。

        参数：
        frame - 原始图像帧
        matched_faces - 一个包含字典的列表，每个字典包含 'bbox' (边界框) 和 'name' (人名)
        """
        annotated_frame = frame.copy()  # 确保不改变原始帧
        for face in matched_faces:
            box = face['bbox']
            name = face['name']

            # 绘制人脸矩形框
            color = (0, 0, 255)  # 红色
            thickness = 2
            cv2.rectangle(annotated_frame, (box[0], box[1]), (box[2], box[3]), color, thickness)

            # 在人脸下方绘制标签
            font = cv2.FONT_HERSHEY_DUPLEX
            font_scale = 1.0
            label_color = (0, 0, 255)  # 红色
            label_thickness = 1

            text_offset_x = box[0]
            text_offset_y = box[3] + 30

            cv2.putText(annotated_frame, name, (text_offset_x, text_offset_y), font, font_scale, color, label_thickness)
            cv2.putText(annotated_frame, name, (text_offset_x, text_offset_y), font, font_scale, label_color, label_thickness)

        # 将处理后的帧加入到队列中
        self.processed_queue.append(annotated_frame)

    def stop(self):
        """
        停止摄像头捕获线程并释放资源
        """
        self.stopped = True
        if self.thread is not None:
            self.thread.join()  # 等待线程结束
        self.cap.release()
        self.thread = None  # 清理线程引用

    def __del__(self):
        """
        析构函数，确保资源释放
        """
        self.stop()