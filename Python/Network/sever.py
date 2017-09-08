# Echo server program
import socket
import time, os


HOST = ''
PORT = 50007

my_dict = {"date": time.ctime, "os": os.name, "ls": lambda x="": ", ".join(os.listdir(os.path.join(os.curdir, x)))}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)
    conn, addr = s.accept()

    with conn:
        print('Connected by', addr)

        while True:
            data = conn.recv(1024)

            if not data:
                break

            cmd_list = data.decode().split()
            cmd_proc = my_dict.get(cmd_list[0])

            if cmd_proc:
                if callable(cmd_proc):
                    if len(cmd_list) > 1:
                        conn.sendall(cmd_proc(cmd_list[1]).encode())
                    else:
                        conn.sendall(cmd_proc().encode())
                else:
                    conn.sendall(cmd_proc.encode())
            else:
                conn.sendall(data)






