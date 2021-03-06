"""
socket 简易服务器和客户端，能够在服务器端执行命令，并把结果回传到客户端
"""
#Server_side_start

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket,os,time
server = socket.socket()
server.bind(('localhost',9999))

server.listen()

while True:
    conn,addr = server.accept()
    print("new conn",addr)
    while True:
        data = conn.recv(8192)
        if not data:
            print("客户端已断开")
            break
        print("执行指令",data)
        cmd_res = os.popen(data.decode()).read() #接收字符串，执行结果也是字符串
        if not cmd_res:
            cmd_res = "cmd has no output"

        conn.send(str(len(cmd_res.encode("utf-8"))).encode("utf-8"))  #先发大小给客户端
        # time.sleep(0.5)
        client_ack = conn.recv(1024) #wait client confirm,解决socket粘包问题
        conn.send(cmd_res.encode("utf-8"))
        print("send done...\n等待新指令...")
server.close()

#Server_side_end

================================分割线===============================

#client_start

#!/usr/bin/env python
# -*- coding:utf-8 -*-

import socket
client = socket.socket()

client.connect(('localhost',9999))

while True:
    cmd = input(">>: ").strip()
    if not cmd: continue
    client.send(cmd.encode("utf-8"))
    cmd_res_size = client.recv(1024) #接收命令结果的长度
    client.send("准备好接收了".encode("utf-8"))
    received_size = 0
    received_data = b''
    while received_size < int(cmd_res_size.decode()) : #判断接收长度，直到接收完毕
        data = client.recv(1024)
        received_size += len(data)
        #print(data.decode())
        received_data += data
    else:
        print(received_data.decode())
        print("cmd res receive done..")        
client.close()

#client_end
