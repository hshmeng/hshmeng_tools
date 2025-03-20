import socket
import threading
import time
import random

class NetworkManager:
    def __init__(self, base_port, broadcast_port):
        self.base_port = base_port
        self.broadcast_port = broadcast_port
        self.udp_socket = None
        self.tcp_socket = None
        self.connections = {}
        self.running = True
        self.lock = threading.Lock()
        self.known_nodes = {}
        self.scan_interval = 15
        self.broadcast_interval = 10
        self.manual_scanning = False
        self.display_message_callback = None  # 用于回调GUI的显示消息方法

    def set_display_message_callback(self, callback):
        """设置回调函数，用于将消息显示在GUI中"""
        self.display_message_callback = callback

    def start_udp_service(self):
        def udp_listener():
            self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.udp_socket.bind(('', self.broadcast_port))

            while self.running:
                try:
                    data, addr = self.udp_socket.recvfrom(1024)
                    if data.startswith(b'P2P_HELLO'):
                        _, port = data.decode().split(':')
                        self.update_node(addr[0], int(port))
                except:
                    pass

        def udp_broadcaster():
            while self.running:
                try:
                    msg = f"P2P_HELLO:{self.base_port}"
                    self.udp_socket.sendto(msg.encode(), ('<broadcast>', self.broadcast_port))
                except Exception as e:
                    print(f"UDP Broadcast Error: {e}")
                time.sleep(self.broadcast_interval)

        threading.Thread(target=udp_listener, daemon=True).start()
        threading.Thread(target=udp_broadcaster, daemon=True).start()

    def start_tcp_server(self):
        def tcp_server():
            self.tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.tcp_socket.bind(('0.0.0.0', self.base_port))
            self.tcp_socket.listen(5)

            while self.running:
                try:
                    conn, addr = self.tcp_socket.accept()
                    threading.Thread(target=self.handle_tcp_connection, args=(conn, addr)).start()
                except:
                    break

        threading.Thread(target=tcp_server, daemon=True).start()

    def start_scanner(self):
        def subnet_scanner():
            while self.running:
                self.scan_subnet()
                time.sleep(self.scan_interval)

        threading.Thread(target=subnet_scanner, daemon=True).start()

    def scan_subnet(self):
        if not self.manual_scanning:
            local_ips = self.get_local_ips()
            for ip in self.generate_subnet_ips(local_ips):
                for port in [self.base_port, self.broadcast_port, 9090]:
                    self.attempt_connect(ip, port)

    def attempt_connect(self, ip, port):
        if (ip, port) in self.connections:
            return
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((ip, port))
            with self.lock:
                self.connections[(ip, port)] = s
            threading.Thread(target=self.handle_tcp_connection, args=(s, (ip, port))).start()
        except Exception as e:
            pass

    def handle_tcp_connection(self, conn, addr):
        conn.settimeout(30)
        try:
            while self.running:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    if self.display_message_callback:
                        self.display_message_callback(f"[{addr[0]}] {data.decode()}")
                except socket.timeout:
                    pass
        except:
            pass
        finally:
            self.remove_connection(addr)

    def remove_connection(self, addr):
        with self.lock:
            if addr in self.connections:
                try:
                    self.connections[addr].close()
                except:
                    pass
                del self.connections[addr]
            if self.display_message_callback:
                self.display_message_callback(f"连接丢失: {addr[0]}:{addr[1]}")

    def start_connection_manager(self):
        def manager():
            while self.running:
                with self.lock:
                    to_remove = [addr for addr, conn in self.connections.items()
                                 if self.check_connection_dead(conn)]
                    for addr in to_remove:
                        self.remove_connection(addr)
                time.sleep(5)

        threading.Thread(target=manager, daemon=True).start()

    def check_connection_dead(self, conn):
        try:
            conn.send(b'')
            return False
        except:
            return True

    def generate_subnet_ips(self, local_ips):
        ips = []
        for ip in local_ips:
            if ip.startswith("127."):
                continue
            octets = ip.split('.')[:3]
            base_ip = '.'.join(octets) + '.'
            ips.extend(f"{base_ip}{i}" for i in range(1, 255))
        return list(set(ips))

    def get_local_ips(self):
        ips = []
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ips.append(s.getsockname()[0])
            s.close()
        except:
            pass
        return ips or ["127.0.0.1"]

    def update_node(self, ip, port):
        self.known_nodes[ip] = time.time()
        self.attempt_connect(ip, port)