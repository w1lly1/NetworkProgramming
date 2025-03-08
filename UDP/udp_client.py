# UDP client

from socket import *

# 服务器地址，本地回环地址Testing
serverName = '127.0.0.1'
# 服务器监听的端口号
serverPort = 8888

# serverName = '10.249.36.186'
# serverPort = 12001

clientSocket = socket(AF_INET, SOCK_DGRAM)
# clientSocket.bind(('127.0.0.1', 5432))

while True:
    msg = input('Input lowercase sentence (type "quit" to exit):')
    clientSocket.sendto(msg.encode(), (serverName, serverPort))
    if msg == 'quit':
        break
    try:
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        print(modifiedMessage.decode())
    except Exception as e:
        print(f"Error receiving message: {e}")

# 关闭套接字
clientSocket.close()