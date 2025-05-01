# import time
# import cv2
# import numpy as np
# import os
# import pyttsx3
# import serial
# from edge_tpu_silva import process_detection

# # Initialize TTS
# engine = pyttsx3.init()
# engine.setProperty('rate', 150)
# engine.setProperty('volume', 1)

# # Initialize Serial
# esp_serial = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
# time.sleep(2)  # Give ESP time to reset

# # Face Recognition Setup
# haar_file = 'haarcascade_frontalface_default.xml'
# datasets = 'datasets'
# print('Initializing face recognition...')

# (images, labels, names, id) = ([], [], {}, 0)
# for (subdirs, dirs, files) in os.walk(datasets):
#     for subdir in dirs:
#         names[id] = subdir
#         subjectpath = os.path.join(datasets, subdir)
#         for filename in os.listdir(subjectpath):
#             path = os.path.join(subjectpath, filename)
#             images.append(cv2.imread(path, 0))
#             labels.append(id)
#         id += 1

# (width, height) = (130, 100)
# (images, labels) = [np.array(lis) for lis in [images, labels]]
# model = cv2.face.LBPHFaceRecognizer_create()
# model.train(images, labels)
# face_cascade = cv2.CascadeClassifier(haar_file)

# # Camera Setup
# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
# frame_width, frame_height = 1280, 720
# center_x = frame_width // 2

# tracking = False
# person_id = None

# print("Waiting for known face...")

# # Face Recognition Loop
# while not tracking:
#     ret, frame = cap.read()
#     if not ret:
#         continue
#     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#     faces = face_cascade.detectMultiScale(gray, 1.3, 5)
#     for (x, y, w, h) in faces:
#         face = gray[y:y + h, x:x + w]
#         face_resize = cv2.resize(face, (width, height))
#         prediction = model.predict(face_resize)
#         if 60 < prediction[1] < 90:
#             person_id = prediction[0]
#             name = names[person_id]
#             print(f"Recognized {name}, beginning tracking.")
#             engine.say(f"Hi {name}, I'm following you.")
#             engine.runAndWait()
#             tracking = True
#             break

# cap.release()

# # Send speed setup once (set to 4)
# esp_serial.write(b'4')
# esp_serial.flush()
# print("Speed set: 4")

# # YOLOv8 Tracking with Edge TPU
# model_path = '240_yolov8n_full_integer_quant_edgetpu.tflite'
# input_source = 0
# recognized_bbox = None
# previous_command = None
# last_send_time = time.time()

# def get_iou(boxA, boxB):
#     xA = max(boxA[0], boxB[0])
#     yA = max(boxA[1], boxB[1])
#     xB = min(boxA[2], boxB[2])
#     yB = min(boxA[3], boxB[3])
#     interArea = max(0, xB - xA) * max(0, yB - yA)
#     boxAArea = (boxA[2] - boxA[0]) * (boxA[3] - boxA[1])
#     boxBArea = (boxB[2] - boxB[0]) * (boxB[3] - boxB[1])
#     return interArea / float(boxAArea + boxBArea - interArea + 1e-5)

# outs = process_detection(
#     model_path=model_path,
#     input_path=input_source,
#     imgsz=240,
#     threshold=0.4,
#     verbose=False,
#     show=True,
#     classes=[0]
# )

# for detections, fps in outs:
#     command = "S"

#     if recognized_bbox is None and detections:
#         min_dist = float('inf')
#         for det in detections:
#             x1, y1, x2, y2 = map(int, det['bbox'])
#             cx = (x1 + x2) // 2
#             cy = (y1 + y2) // 2
#             dist = ((cx - center_x) ** 2 + (cy - (frame_height // 2)) ** 2) ** 0.5
#             if dist < min_dist:
#                 min_dist = dist
#                 recognized_bbox = (x1, y1, x2, y2)

#     target_det = None
#     best_iou = 0
#     for det in detections:
#         bbox = tuple(map(int, det['bbox']))
#         iou = get_iou(bbox, recognized_bbox)
#         if iou > best_iou:
#             best_iou = iou
#             target_det = bbox

#     if target_det is not None:
#         x1, y1, x2, y2 = target_det
#         recognized_bbox = target_det
#         person_height = y2 - y1
#         person_center_x = (x1 + x2) // 2
#         vertical_ratio = person_height / frame_height

#         if vertical_ratio <= 0.50:
#             command = "F"
#         elif vertical_ratio >= 0.65:
#             command = "B"
#         else:
#             if person_center_x <= 189:
#                 command = "L"
#             elif person_center_x >= 422:
#                 command = "R"
#             else:
#                 command = "S"
#     else:
#         command = "S"

#     # Send command every 1 second
#     current_time = time.time()
#     if current_time - last_send_time >= 1:
#         esp_serial.write(command.encode())
#         esp_serial.flush()
#         print(f"Command sent: {command}")

#         if command in ["L", "R"]:
#             # Adding delay of 200ms after sending "L" or "R"
#             time.sleep(0.2)
#             esp_serial.write(b"S")
#             esp_serial.flush()
#             print("Sent 'S' after delay.")

#         last_send_time = current_time

# print("Tracking stopped.")


while(1):
    print("Hiii")