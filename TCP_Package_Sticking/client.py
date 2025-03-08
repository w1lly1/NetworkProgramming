import socket
import struct

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 8888))

    # 模拟粘包问题
    data = client_socket.recv(1024)
    print(f"Received raw data (sticky packet): {data}")  # 输出：b'HelloWorld'

    # 解决粘包问题
    message1 = receive_message(client_socket)
    message2 = receive_message(client_socket)
    print(f"Received message 1: {message1}")  # 输出：b'Hello'
    print(f"Received message 2: {message2}")  # 输出：b'World'

    client_socket.close()

def receive_message(sock):
    # 先读取4字节的消息头
    header = sock.recv(4)
    if not header:
        return None
    # 解析消息头，获取消息体长度
    message_length = struct.unpack('!I', header)[0]
    # 根据长度读取消息体
    message = b''
    while len(message) < message_length:
        chunk = sock.recv(message_length - len(message))
        if not chunk:
            break
        message += chunk
    return message

if __name__ == "__main__":
    start_client()