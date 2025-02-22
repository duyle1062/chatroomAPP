import threading
import socket
import argparse
import os
import sys
import tkinter as tk

class Receive(threading.Thread):
    def __init__(self, sock, name):
        super().__init__()
        self.sock = sock
        self.name = name
        self.messages = None

    def run(self):
        while True:
            try:
                message = self.sock.recv(1024).decode('ascii')
                if message:
                    if self.messages:
                        self.messages.insert(tk.END, message)
                    print(f'\r{message}\n{self.name}: ', end='')
                else:
                    print('\nConnection lost!')
                    self.sock.close()
                    os._exit(0)
            except ConnectionResetError:
                print('\nConnection lost!')
                self.sock.close()
                os._exit(0)

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.name = None
        self.messages = None

    def start(self):
        print(f'Trying to connect to {self.host}:{self.port}...')
        self.sock.connect((self.host, self.port))
        print(f'Successfully connected to {self.host}:{self.port}\n')

        self.name = input('Your name: ')
        print(f'Welcome, {self.name}!')

        receive = Receive(self.sock, self.name)
        receive.start()

        self.sock.sendall(f'Server: {self.name} has joined the chat.'.encode('ascii'))
        print("\rReady! Type 'QUIT' to leave.\n")
        print(f'{self.name}: ', end='')

        return receive

    def send(self, textInput):
        message = textInput.get()
        textInput.delete(0, tk.END)
        self.messages.insert(tk.END, f'{self.name}: {message}')

        if message == "QUIT":
            self.sock.sendall(f'Server: {self.name} has left the chat.'.encode('ascii'))
            print('\nQuitting...')
            self.sock.close()
            os._exit(0)
        else:
            self.sock.sendall(f'{self.name}: {message}'.encode('ascii'))

def main(host, port):
    client = Client(host, port)
    receive = client.start()

    window = tk.Tk()
    window.title(f"Chatroom - {client.name}")

    fromMessage = tk.Frame(master=window)
    scrollBar = tk.Scrollbar(master=fromMessage)
    messages = tk.Listbox(master=fromMessage, yscrollcommand=scrollBar.set)
    scrollBar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
    messages.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    client.messages = messages
    receive.messages = messages

    fromMessage.grid(row=0, column=0, columnspan=2, sticky="nsew")
    fromEntry = tk.Frame(master=window)
    textInput = tk.Entry(master=fromEntry)

    textInput.pack(fill=tk.BOTH, expand=True)
    textInput.bind("<Return>", lambda x: client.send(textInput))
    textInput.insert(0, "Write your message here")

    btnSend = tk.Button(master=window, text='Send', command=lambda: client.send(textInput))

    fromEntry.grid(row=1, column=0, padx=10, sticky="ew")
    btnSend.grid(row=1, column=1, pady=10, sticky="ew")

    window.rowconfigure(0, weight=4)  
    window.rowconfigure(1, weight=1)  

    window.columnconfigure(0, weight=3)  
    window.columnconfigure(1, weight=1)  


    window.mainloop()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Chatroom Client")
    parser.add_argument('host', help='Server IP address')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060, help='TCP port (default 1060)')

    args = parser.parse_args()
    main(args.host, args.p)
