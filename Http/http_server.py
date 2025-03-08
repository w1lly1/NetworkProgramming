from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = 80
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.listen(1)
print('The server is ready to receive')

while True:
    connectionSocket, addr = serverSocket.accept()
    sentence = connectionSocket.recv(1024).decode()

    if not sentence or sentence == 'quit':
        break

    try:
        import os
        script_dir = os.path.dirname(os.path.abspath(__file__))
        filename = sentence.split()[1] # /hello.html
        file_path = os.path.join(script_dir, filename[1:])
        f = open(file_path) # hello.html
        outputdata = f.read()
        outputdata = 'HTTP/1.1 200 OK\r\n\r\n' + outputdata
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.close()
        print('200 OK')
        f.close()
        break;
    except IOError:
        outputdata = 'HTTP/1.1 404 Not Found\r\n\r\n'
        for i in range(0, len(outputdata)):
            connectionSocket.send(outputdata[i].encode())
        connectionSocket.close()
        break;

serverSocket.close()