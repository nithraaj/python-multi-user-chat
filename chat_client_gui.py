import socket
import select
import sys
from tkinter import *
from _thread import *

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
class ChatFrame():
    def __init__(self, top):
        self.top = top
        self.frame = Frame(self.top)
        self.frame.grid()
        self.messages = Text(self.frame)
        self.messages.pack()
        self.input_user = StringVar()
        self.input_field = Entry(self.frame, text=self.input_user)
        self.input_field.pack(side=BOTTOM, fill=X)
        self.input_field.bind("<Return>", self.Enter_pressed)
        return
    def Enter_pressed(self,event):
        input_get = self.input_field.get()
        self.addMessage("You: "+input_get)
        self.input_user.set('')
        server.send(input_get.encode())
        return "break"
    def addMessage(self, message):
        self.messages.insert(INSERT, '%s\n' % message)

class ConnectFrame():
    def __init__(self, top):
        self.top=top
        self.top.geometry("+10+10")
        self.frame=Frame(self.top)
        self.frame.grid()
        self.lbl_title = Label(self.frame, text = "Welcome to Chatty", font = ("Arial Bold",20))
        self.lbl_title.grid(column = 0, row = 0, columnspan = 2, ipadx = 30)

        self.lbl_ip = Label(self.frame, text = "Server IP")
        self.lbl_ip.grid(column = 0, row = 1, sticky='W', pady = 20, padx = 3)
        self.txt_ip = Entry(self.frame, width = 15)
        self.txt_ip.grid(column = 1, row = 1, sticky='W', pady = 20)

        self.lbl_port = Label(self.frame, text = "Server port")
        self.lbl_port.grid(column = 0, row = 2, sticky='W', padx = 3)
        self.txt_port = Entry(self.frame, width = 5)
        self.txt_port.grid(column = 1, row = 2, sticky='W')

        self.btn = Button(self.frame, text = "Connect", bg = "black", fg = "white", command = self.connect, font = ("Arial",14))
        self.btn.grid(column = 0, row = 3, columnspan = 2, pady = 20)

    def destroy(self):
        self.frame.destroy()
        self.chat_frame=ChatFrame(self.top)
        start_new_thread(self.listen,())
    def connect(self):
        ip = self.txt_ip.get()
        port = int(self.txt_port.get())
        server.connect((ip,port))
        self.destroy()
    def listen(self):
        while True:
            sockets_list = [sys.stdin, server]
            read_sockets,write_socket, error_socket = select.select(sockets_list,[],[]) 
            for socks in read_sockets: 
                if socks == server: 
                    message = socks.recv(1024) 
                    if message:
                        self.chat_frame.addMessage(message.decode())
                    else:
                        print("Server probably closed connection")
                        exit(0)


root = Tk()
root.title("Chatty")
CF = ConnectFrame(root)
root.mainloop()