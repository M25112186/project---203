import socket
from threading import Thread
from tkinter import *

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ip_address = '127.0.0.1'
port = 8000

client.connect((ip_address, port))

print("Connected with the server...")

class GUI:
    def __init__(self):
        self.window = Tk()
        self.window.withdraw()

        self.login = Toplevel()
        self.login.title("Login")

        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=300, bg="#ADD8E6")
        
        self.pls = Label(self.login,
                         text="Please login to continue",
                         justify=CENTER,
                         font="Helvetica 14 bold",
                         bg="#ADD8E6",
                         fg="#00008B")
        self.pls.place(relheight=0.15, relx=0.2, rely=0.07)

        self.labelName = Label(self.login,
                               text="Name: ",
                               font="Helvetica 12",
                               bg="#ADD8E6",
                               fg="#00008B")
        self.labelName.place(relheight=0.2, relx=0.1, rely=0.2)

        self.entryName = Entry(self.login,
                               font="Helvetica 14",
                               bg="#E6F0FA",
                               fg="#00008B",
                               bd=0,
                               highlightthickness=1,
                               highlightbackground="#00008B",
                               highlightcolor="#00008B")
        self.entryName.place(relwidth=0.4, relheight=0.12, relx=0.35, rely=0.2)
        self.entryName.focus()

        self.go = Button(self.login,
                         text="CONTINUE",
                         font="Helvetica 14 bold",
                         bg="#B0E0E6",
                         fg="#00008B",
                         activebackground="#87CEEB",
                         activeforeground="#00008B",
                         bd=0,
                         command=lambda: self.goAhead(self.entryName.get()))
        self.go.place(relx=0.4, rely=0.55, relwidth=0.3, relheight=0.1)
        self.go.configure(cursor="hand2")

        self.window.mainloop()

    def goAhead(self, name):
        self.login.destroy()
        self.layout(name)
        rcv = Thread(target=self.receive)
        rcv.start()

    def receive(self):
        while True:
            try:
                message = client.recv(2048).decode('utf-8')
                if message == 'NICKNAME':
                    client.send(self.name.encode('utf-8'))
                else:
                    self.show_message(message)
            except:
                print("An error occurred!")
                client.close()
                break
    
    def layout(self, name):
        self.name = name
        self.window.deiconify()
        self.window.title("Chatroom")
        self.window.configure(width=470, height=550, bg="#E6F0FA")
        self.window.resizable(width=False, height=False)

        self.labelHead = Label(self.window,
                               bg="#ADD8E6",
                               fg="#00008B",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)
        self.labelHead.place(relwidth=1)
        
        self.line = Label(self.window,
                          width=450,
                          bg="#B0E0E6")
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        self.textCons = Text(self.window,
                             width=20,
                             height=2,
                             bg="#E6F0FA",
                             fg="#00008B",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)
        self.textCons.place(relheight=0.745, relwidth=1, rely=0.08)
        
        self.labelBottom = Label(self.window, bg="#B0E0E6", height=80)
        self.labelBottom.place(relwidth=1, rely=0.825)
        
        self.entryMsg = Entry(self.labelBottom,
                              bg="#ADD8E6",
                              fg="#00008B",
                              font="Helvetica 13",
                              bd=0,
                              highlightthickness=1,
                              highlightbackground="#00008B",
                              highlightcolor="#00008B")
        self.entryMsg.place(relwidth=0.74, relheight=0.06, rely=0.008, relx=0.011)
        self.entryMsg.focus()
        
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#87CEEB",
                                fg="#00008B",
                                activebackground="#B0E0E6",
                                activeforeground="#00008B",
                                bd=0,
                                command=lambda: self.sendButton(self.entryMsg.get()))
        self.buttonMsg.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)
        
        scrollbar = Scrollbar(self.textCons)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.textCons.yview)
        self.textCons.config(state=DISABLED)

    def sendButton(self, msg):
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = Thread(target=self.write)
        snd.start()

    def show_message(self, message):
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, message + "\n\n")
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)

    def write(self):
        while True:
            message = f"{self.name}: {self.msg}"
            client.send(message.encode('utf-8'))
            self.show_message(message)
            break

g = GUI()
