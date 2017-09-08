# Echo client program
import socket

HOST = 'localhost'
PORT = 50007

cmds = ("date", "os", "ls", "ls test_directory")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    for cmd in cmds:
        s.sendall(cmd.encode())
        data = s.recv(1024)
        print('Received', data.decode())






