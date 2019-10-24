import socket 
import select 
import sys 
from _thread import *
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
if len(sys.argv) != 3: 
    print("Correct usage: script, IP address, port number")
    exit()
IP_address = str(sys.argv[1])
Port = int(sys.argv[2])
server.bind((IP_address, Port))
server.listen(100) 
list_of_clients = [] 
def clientthread(conn, addr):
    conn.send("Server: Welcome to this chat room".encode()) 
    while True: 
        try: 
            # print("waiting for client..."+str(addr))
            message = conn.recv(1024)
            message = message.decode("utf-8")
            if message:
                print("<" + addr[0] + ":" + str(addr[1]) + "> " + message)
                message_to_send = "<" + addr[0] + ":" + str(addr[1]) + "> " + message 
                broadcast(message_to_send.encode(), conn) 
            else:
                print("removing conn")
                remove(conn)
                break
        except: 
            print("exception:"+str(sys.exc_info()))
            break
    print("closing client thread")
def broadcast(message, connection): 
    for client in list_of_clients: 
        if client!=connection: 
            try: 
                client.send(message) 
            except: 
                client.close() 
                print("closing client:"+client)
                remove(client)
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 
while True: 
    conn, addr = server.accept() 
    list_of_clients.append(conn)
    print(addr[0]+ ":" + str(addr[1]) + " connected")
    start_new_thread(clientthread,(conn,addr))
server.close() 