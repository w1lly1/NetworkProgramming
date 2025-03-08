import socket
import struct

def start_server():
    # 创建TCP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('127.0.0.1', 8888))
    server_socket.listen(5)
    print("Server started, waiting for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr} established.")

        # 模拟粘包问题
        data1 = b"Hello"
        data2 = b"World"
        client_socket.send(data1 + data2)  # 两个消息粘在一起发送

        # 使用消息头+消息体解决粘包问题
        message1 = b"Hello"
        message2 = b"World"
        send_message(client_socket, message1)
        send_message(client_socket, message2)

        client_socket.close()

def send_message(sock, message):
    # 消息头：4字节，表示消息体长度
    header = struct.pack('!I', len(message))
    # 发送消息头 + 消息体
    sock.send(header + message)

if __name__ == "__main__":
    start_server()