# tcp client

from socket import *

serverName = '127.0.0.1'

# serverName = '10.249.37.49'
serverPort = 12002

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:
    msg = input('Input lowercase sentence (type "quit" to exit):')
    clientSocket.send(msg.encode())
    if msg == 'quit':
        break
    try:
        modifiedMessage = clientSocket.recv(1024)
        print(modifiedMessage.decode())
    except Exception as e:
        print(f"Error receiving message: {e}")

clientSocket.close()