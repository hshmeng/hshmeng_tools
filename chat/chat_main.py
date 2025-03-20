import socket
import threading

# 默认端口
PORT = 8070

# 处理接收消息的函数
def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024).decode('utf-8')
            if not data:
                break
            print(f"Received: {data}")
        except:
            break

# 处理发送消息的函数
def send_messages(sock):
    while True:
        message = input()
        sock.send(message.encode('utf-8'))

# 启动服务器
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('0.0.0.0', PORT))
    server_socket.listen(5)
    print(f"Server started on port {PORT}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Connection from {addr}")
        threading.Thread(target=receive_messages, args=(client_socket,)).start()

# 连接到其他客户端
def connect_to_client(ip):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((ip, PORT))
    print(f"Connected to {ip}")
    threading.Thread(target=receive_messages, args=(client_socket,)).start()
    threading.Thread(target=send_messages, args=(client_socket,)).start()

if __name__ == "__main__":
    # 启动服务器线程
    server_thread = threading.Thread(target=start_server)
    server_thread.daemon = True
    server_thread.start()

    # 连接到其他客户端
    target_ip = input("Enter the IP address to connect to: ")
    connect_to_client(target_ip)