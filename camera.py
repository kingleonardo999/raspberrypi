import cv2
import threading
from queue import Queue

class Camera:
    def __init__(self, src=0):
        self.cap = cv2.VideoCapture(src)  # 打开摄像头
        if not self.cap.isOpened():
            raise ValueError("无法打开摄像头，请检查摄像头索引或连接")
        self.thread = None  # 初始化 thread 属性
        self.frame = None
        self.queue = Queue()
        self.stopped = False

    def start(self):
        if not self.thread:  # 只有当线程未启动时才启动新线程
            self.thread = threading.Thread(target=self.update, args=())
            self.thread.daemon = True  # 设置为守护线程
            self.thread.start()

    def update(self):
        while not self.stopped:
            ret, frame = self.cap.read()
            if ret:
                self.queue.put(frame)
            else:
                print("无法抓取帧")
                break

    def read(self):
        return self.queue.get()

    def stop(self):
        self.stopped = True
        if self.thread is not None:
            self.thread.join()  # 等待线程结束
        self.cap.release()
        self.thread = None  # 清理线程引用

    def __del__(self):
        self.stop()


if __name__ == '__main__':
    cam = Camera()
    cam.start()
    while True:
        frame = cam.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cam.stop()
    cv2.destroyAllWindows()