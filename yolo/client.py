import socket
import numpy as np
import cv2 as cv
import json
from PIL import Image
from tts import TTS

IP = '127.0.0.1'
Port = 9999

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, Port))
print("server와 연결완료.")
while True:
    image_name = input("image 파일 이름(xxx.jpg) / exit (종료) : ")
    if image_name == "exit":
        client_socket.send(str(int(len(image_name))).encode())
        client_socket.send(image_name.encode())
        break
    image = cv.imread(image_name)
    stringData = cv.imencode('.jpg', image)[1].tostring()
    client_socket.send(str(len(stringData)).ljust(16).encode())
    client_socket.send(stringData)
    response = client_socket.recv(1024)
    response = response.decode()
    TTS(response)

client_socket.close()
