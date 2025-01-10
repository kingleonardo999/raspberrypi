import cv2
import pickle

cap = cv2.VideoCapture(0)

face_casecade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_alt2.xml')

# 加载人脸识别模型
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")

labels = {}
# 加载对应关系
with open("labels.pickle", "rb") as f:
    origin_labels = pickle.load(f) # {name: id}
    labels = {v: k for k, v in origin_labels.items()} # {id: name}

while True:
    ret, frame = cap.read()
    if ret:
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_casecade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)

        for (x, y, w, h) in faces:
            gray_roi = gray[y:y+h, x:x+w]
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # 将人脸区域丢入预测
            id_, conf = recognizer.predict(gray_roi)
            name = labels[id_]
            if conf >= 60:
                cv2.putText(frame, name, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

        cv2.imshow('Result', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()