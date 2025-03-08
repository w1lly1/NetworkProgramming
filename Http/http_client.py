from socket import *

serverName = "10.249.37.49"
# serverName = "127.0.0.1"
serverPort = 80

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

outputdata = "GET /hello.html HTTP/1.1\r\nHost: 10.249.37.49\r\n\r\n"
clientSocket.send(outputdata.encode())

data = 2
while data:
    data = clientSocket.recv(1024)
    print(data.decode())

clientSocket.close()