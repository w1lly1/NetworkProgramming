import socket
import base64
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler()]
)

# 邮件服务器配置
SMTP_SERVER = "smtp.163.com"  # 网易163邮箱服务器
SMTP_PORT = 25                # SMTP端口（25或587）
SENDER_EMAIL = "tliangy@163.com"  # 发件人邮箱
SENDER_PASSWORD = "ECb2v5U9QfyfQCAg"    # 发件人邮箱密码（或授权码）
RECIPIENT_EMAIL = "biz_will_yi@163.com"  # 收件人邮箱

# 邮件内容
SUBJECT = "Test Email from SMTP Client"
BODY = "Hello, this is a test email sent from a Python SMTP client."

def send_email():
    client_socket = None
    try:
        # 创建TCP连接
        logging.info("Step 1: Connecting to SMTP server...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SMTP_SERVER, SMTP_PORT))
        response = client_socket.recv(1024).decode()
        logging.info(f"Server Response: {response}")

        # 发送HELO命令
        logging.info("Step 2: Sending HELO command...")
        helo_command = f"HELO {SMTP_SERVER}\r\n"
        client_socket.send(helo_command.encode())
        response = client_socket.recv(1024).decode()
        logging.info(f"Server Response: {response}")

        # 登录认证
        logging.info("Step 3: Authenticating...")
        auth_command = "AUTH LOGIN\r\n"
        client_socket.send(auth_command.encode())
        response = client_socket.recv(1024).decode()
        logging.info(f"Server Response: {response}")

        # 发送用户名（Base64编码）
        logging.info("Step 4: Sending username...")
        username = base64.b64encode(SENDER_EMAIL.encode()).decode()
        client_socket.send(f"{username}\r\n".encode())
        response = client_socket.recv(1024).decode()
        logging.info(f"Server Response: {response}")

        # 发送密码（Base64编码）
        logging.info("Step 5: Sending password...")
        password = base64.b64encode(SENDER_PASSWORD.encode()).decode()
        client_socket.send(f"{password}\r\n".encode())
        response = client_socket.recv(1024).decode()
        logging.info(f"Server Response: {response}")

        # 指定发件人
        logging.info("Step 6: Specifying sender...")
        mail_from_command = f"MAIL FROM: <{SENDER_EMAIL}>\r\n"
        client_socket.send(mail_from_command.encode())
        response = client_socket.recv(1024).decode()
        logging.info(f"Server Response: {response}")

        # 指定收件人
        logging.info("Step 7: Specifying recipient...")
        rcpt_to_command = f"RCPT TO: <{RECIPIENT_EMAIL}>\r\n"
        client_socket.send(rcpt_to_command.encode())
        response = client_socket.recv(1024).decode()
        logging.info(f"Server Response: {response}")

        # 发送邮件内容
        logging.info("Step 8: Sending email content...")
        data_command = "DATA\r\n"
        client_socket.send(data_command.encode())
        response = client_socket.recv(1024).decode()
        logging.info(f"Server Response: {response}")

        # 邮件正文
        email_content = f"Subject: {SUBJECT}\r\n\r\n{BODY}\r\n.\r\n"
        client_socket.send(email_content.encode())
        response = client_socket.recv(1024).decode()
        logging.info(f"Server Response: {response}")

        # 关闭连接
        logging.info("Step 9: Closing connection...")
        quit_command = "QUIT\r\n"
        client_socket.send(quit_command.encode())
        response = client_socket.recv(1024).decode()
        logging.info(f"Server Response: {response}")

        logging.info("Email sent successfully!")

    except Exception as e:
        logging.error(f"Error occurred: {e}", exc_info=True)
    finally:
        if client_socket:
            client_socket.close()
            logging.info("TCP connection closed.")

if __name__ == "__main__":
    send_email()