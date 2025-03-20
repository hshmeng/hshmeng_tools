import socket
import threading
import sys


class P2PChat:
    def __init__(self, port=8070):
        self.port = port
        self.connections = []
        self.running = True
        self.lock = threading.Lock()
        self.server_socket = None

    def start(self):
        # 启动服务器线程
        server_thread = threading.Thread(target=self.start_server)
        server_thread.daemon = True
        server_thread.start()

        # 启动输入处理
        self.input_handler()

    def start_server(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind(('0.0.0.0', self.port))
        self.server_socket.listen(5)
        print(f"服务器已启动，监听端口 {self.port}")

        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                with self.lock:
                    self.connections.append(conn)
                print(f"\n新连接来自 {addr}")
                client_thread = threading.Thread(target=self.handle_client, args=(conn, addr))
                client_thread.start()
            except:
                break

    def handle_client(self, conn, addr):
        try:
            while self.running:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode()
                print(f"\n来自 {addr}: {message}")
        except:
            pass
        finally:
            with self.lock:
                self.connections.remove(conn)
            conn.close()
            print(f"\n连接 {addr} 已断开")

    def connect_to_peer(self, ip):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((ip, self.port))
            with self.lock:
                self.connections.append(sock)
            print(f"成功连接到 {ip}:{self.port}")
            # 启动接收线程
            client_thread = threading.Thread(target=self.handle_client, args=(sock, (ip, self.port)))
            client_thread.start()
        except Exception as e:
            print(f"无法连接到 {ip}:{self.port} - {str(e)}")

    def send_message(self, message):
        with self.lock:
            # 过滤掉已关闭的连接
            self.connections = [conn for conn in self.connections if not conn._closed]

            for conn in self.connections:
                try:
                    conn.sendall(message.encode())
                except:
                    self.connections.remove(conn)

    def input_handler(self):
        print("\n命令列表：")
        print("/connect <IP>  - 连接到指定IP的节点")
        print("/exit         - 退出程序")
        while self.running:
            try:
                msg = input()
                if msg.lower().startswith('/connect'):
                    _, ip = msg.split()
                    self.connect_to_peer(ip)
                elif msg.lower() == '/exit':
                    self.shutdown()
                else:
                    self.send_message(msg)
            except Exception as e:
                print(f"输入错误: {str(e)}")

    def shutdown(self):
        self.running = False
        # 关闭所有连接
        with self.lock:
            for conn in self.connections:
                try:
                    conn.close()
                except:
                    pass
            self.connections = []
        # 关闭服务器socket
        if self.server_socket:
            self.server_socket.close()
        print("程序已关闭")
        sys.exit(0)


if __name__ == "__main__":
    chat = P2PChat()
    try:
        chat.start()
    except KeyboardInterrupt:
        chat.shutdown()