import cv2
import os
from insightface.app import FaceAnalysis
from scipy.spatial.distance import cosine
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import matplotlib

# Change the Matplotlib backend
matplotlib.use('TkAgg')

# Initialize InsightFace application
app = FaceAnalysis(providers=['CUDAExecutionProvider', 'CPUExecutionProvider'])
app.prepare(ctx_id=0, det_size=(640, 640))

# Load known face images and learn them
known_face_encodings = []
known_face_names = []
current_file_path = os.path.dirname(os.path.abspath(__file__))
known_people_dir = current_file_path + "/known_people"

for filename in os.listdir(known_people_dir):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        img_path = os.path.join(known_people_dir, filename)
        img = cv2.imread(img_path)
        faces = app.get(img)
        if faces:
            known_face_encodings.append(faces[0].embedding)
            known_face_names.append(filename.split('.')[0])  # Assume the filename is the person's name

# Initialize the camera
video_capture = cv2.VideoCapture(0)

fig, ax = plt.subplots()
im = ax.imshow(np.zeros((480, 640, 3), dtype=np.uint8))

def update_frame(*args):
    ret, frame = video_capture.read()
    if not ret:
        return im,

    # Detect faces in the current frame
    faces = app.get(frame)

    for face in faces:
        embedding = face.embedding
        name = "Unknown"

        # Calculate similarity with known faces
        similarities = [1 - cosine(embedding, known_face) for known_face in known_face_encodings]
        if similarities:
            best_match_index = similarities.index(max(similarities))
            if similarities[best_match_index] > 0.6:  # Set a similarity threshold
                name = known_face_names[best_match_index]

        # Draw a rectangle around the face
        box = face.bbox.astype(int)
        cv2.rectangle(frame, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)

        # Draw a label
        cv2.rectangle(frame, (box[0], box[3] - 35), (box[2], box[3]), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (box[0] + 6, box[3] - 6), font, 1.0, (255, 255, 255), 1)

    im.set_array(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    return im,

ani = animation.FuncAnimation(fig, update_frame, interval=50)
plt.axis('off')
plt.show()

# Release the camera and close all windows
video_capture.release()
cv2.destroyAllWindows()