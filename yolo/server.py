import socket
import numpy as np
import cv2 as cv
from PIL import Image
import json
from yolo import YOLO
## Error/Warning not show!!
import warnings , os
warnings.filterwarnings(action='ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.logging.set_verbosity(tf.logging.ERROR)

IP = '127.0.0.1'
Port = 9999
yolo = YOLO(**{'image': True})
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
print("socket 생성완료.")
server_socket.bind((IP, Port))
print("socket 바인드 완료")
server_socket.listen()
print("socket listening")
client_socket, addr = server_socket.accept()
print("client와 연결완료")

while True:
    length = client_socket.recv(16)
    try:
        data = client_socket.recv(int(length))
        data = np.fromstring(data, dtype=np.uint8)
        decimg = cv.imdecode(data, cv.IMREAD_COLOR)
        image = cv.cvtColor(decimg, cv.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        r_image, detected_list = yolo.detect_image(image)
        response = json.dumps(detected_list)
        #response = np.array(response)
        client_socket.send(response.encode())
    except:
        print("서버 종료")
        yolo.close_session()
        server_socket.close()
        exit(0)