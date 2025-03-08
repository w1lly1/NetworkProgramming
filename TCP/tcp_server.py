# tcp_server.py

from socket import *

serverPort = 12001
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.listen(300)
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()

    if not sentence or sentence == 'quit':
        break

    capitalizedSentence = sentence.upper()
    print(f' recv {capitalizedSentence} from {addr}')
    connectionSocket.send(capitalizedSentence.encode())

connectionSocket.close()
