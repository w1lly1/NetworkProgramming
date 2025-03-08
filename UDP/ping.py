import socket
import time

# 服务器地址和端口
# server_address = ('127.0.0.1', 8888)
server_address = ('10.249.37.49', 12005)
# 创建 UDP 套接字
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 设置超时时间为 1 秒
client_socket.settimeout(1)

# 发送 10 个 ping 报文
for sequence_number in range(1, 11):
    # 记录发送时间
    send_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
    # 构造 ping 报文
    message = f'Ping {sequence_number} {send_time}'
    try:
        # 发送 ping 报文
        client_socket.sendto(message.encode(), server_address)
        # 接收服务器响应
        data, server = client_socket.recvfrom(1024)
        # 记录接收时间
        receive_time = time.time()
        # 将 send_time 转换为时间戳
        send_timestamp = time.mktime(time.strptime(send_time, "%Y-%m-%d-%H-%M-%S"))
        # 计算往返时延（RTT）
        rtt = receive_time - send_timestamp
        # 打印响应信息和 RTT
        print(f'Received from {server}: {data.decode()}, RTT: {rtt:.3f} seconds')
    except socket.timeout:
        # 超时处理，认为报文丢失
        print(f'Ping {sequence_number} Request timed out')

# 发送结束指令
client_socket.sendto('quit'.encode(), server_address)
# 关闭套接字
client_socket.close()