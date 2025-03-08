import socket
import threading

# 代理服务器的配置
PROXY_HOST = '0.0.0.0'  # 代理服务器监听的IP地址
PROXY_PORT = 8888       # 代理服务器监听的端口

# 缓存字典（可选，用于缓存服务器响应）
cache = {}

def handle_client(client_socket):
    """
    处理客户端请求的函数
    """
    # 接收客户端请求数据
    request_data = client_socket.recv(4096).decode()
    print(f"Received request:\n{request_data}")

    # 解析HTTP请求
    first_line = request_data.split('\n')[0]
    method, url, http_version = first_line.split()

    # 提取目标服务器的地址和路径
    if url.startswith("http://"):
        url = url[7:]  # 去掉"http://"
    host_end = url.find('/')
    if host_end == -1:
        host = url
        path = '/'
    else:
        host = url[:host_end]
        path = url[host_end:]

    # 检查缓存中是否有该请求的响应
    if url in cache:
        print("Serving from cache...")
        client_socket.sendall(cache[url])
        client_socket.close()
        return

    # 创建到目标服务器的连接
    try:
        # 创建socket连接到目标服务器
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((host, 80))

        # 构造转发请求
        request = f"{method} {path} {http_version}\r\n"
        request += f"Host: {host}\r\n"
        request += "Connection: close\r\n"
        request += "\r\n"

        # 发送请求到目标服务器
        server_socket.sendall(request.encode())

        # 接收目标服务器的响应
        response_data = b""
        while True:
            data = server_socket.recv(4096)
            if not data:
                break
            response_data += data

        # 将响应存入缓存
        cache[url] = response_data

        # 将响应返回给客户端
        client_socket.sendall(response_data)

    except Exception as e:
        print(f"Error: {e}")
        # 返回500错误
        response = "HTTP/1.1 500 Internal Server Error\r\n\r\n"
        client_socket.sendall(response.encode())

    finally:
        # 关闭连接
        client_socket.close()
        server_socket.close()

def start_proxy():
    """
    启动代理服务器
    """
    # 创建socket对象
    proxy_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_socket.bind((PROXY_HOST, PROXY_PORT))
    proxy_socket.listen(5)
    print(f"Proxy server started on {PROXY_HOST}:{PROXY_PORT}")

    while True:
        # 等待客户端连接
        client_socket, client_address = proxy_socket.accept()
        print(f"Accepted connection from {client_address}")

        # 创建一个新线程处理客户端请求
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

if __name__ == "__main__":
    start_proxy()