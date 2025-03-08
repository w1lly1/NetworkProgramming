# UDP server

from socket import *

serverPort = 8888

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(('127.0.0.1', serverPort))
print('The server is ready to receive')

while True:
    message, clientAddress = serverSocket.recvfrom(2048)
    decoded_message = message.decode()
    # 检查是否接收到 'quit' 指令
    if decoded_message == 'quit':
        print('Server is shutting down...')
        break
    else:
        print(f'Received message: {decoded_message} from {clientAddress}')
    modifiedMessage = decoded_message.upper()
    serverSocket.sendto(modifiedMessage.encode(), clientAddress)

# 关闭套接字
serverSocket.close()