import socket
import threading
import sys
import time
from queue import Queue
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import random


class P2PChatAuto:
    def __init__(self):
        # 网络配置
        self.base_port = random.randint(9000, 9999)  # 随机基础端口
        self.broadcast_port = 9099  # 固定广播端口
        self.udp_socket = None
        self.tcp_socket = None
        self.connections = {}
        self.running = True
        self.lock = threading.Lock()

        # 自动发现配置
        self.scan_interval = 15  # 全子网扫描间隔
        self.broadcast_interval = 10  # 广播发送间隔
        self.known_nodes = {}  # {ip: last_seen_timestamp}
        self.manual_scanning = False  # 新增手动扫描标志

        # GUI初始化
        self.root = tk.Tk()
        self.root.title("HSHMENG Chat")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.create_widgets()

        # 启动核心服务
        self.start_tcp_server()
        self.start_udp_service()
        self.start_scanner()
        self.start_connection_manager()
        self.gui_updater()

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 在线列表
        online_frame = ttk.LabelFrame(main_frame, text="活跃节点")
        online_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.node_list = ttk.Treeview(online_frame, columns=('ip', 'status'), show='headings')
        self.node_list.heading('ip', text='IP地址')
        self.node_list.heading('status', text='状态')
        self.node_list.pack(fill=tk.BOTH, expand=True)

        # 按钮区域
        button_frame = ttk.Frame(online_frame)
        button_frame.pack(fill=tk.X, pady=5)

        ttk.Button(button_frame, text="选择IP", command=self.show_ip_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="关于", command=self.show_about).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="退出", command=self.on_closing).pack(side=tk.RIGHT, padx=2)

        # 聊天区域
        chat_frame = ttk.LabelFrame(main_frame, text="消息")
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.chat_area = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, state='disabled')
        self.chat_area.pack(fill=tk.BOTH, expand=True)

        # 输入框
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)

        self.input_entry = ttk.Entry(input_frame)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_entry.bind("<Return>", lambda e: self.send_message())

        ttk.Button(input_frame, text="发送", command=self.send_message).pack(side=tk.RIGHT)

    # ================= 核心网络功能 =================
    def start_udp_service(self):
        """启动UDP广播服务"""

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
        """启动TCP消息服务器"""

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
        """持续扫描网络"""

        def subnet_scanner():
            while self.running:
                self.scan_subnet()
                time.sleep(self.scan_interval)

        threading.Thread(target=subnet_scanner, daemon=True).start()

    def scan_subnet(self):
        """扫描本地子网"""
        if not self.manual_scanning:
            local_ips = self.get_local_ips()
            for ip in self.generate_subnet_ips(local_ips):
                for port in [self.base_port, self.broadcast_port, 9090]:
                    self.attempt_connect(ip, port)

    def attempt_connect(self, ip, port):
        """优化 TCP 连接尝试"""
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

    # ================= 连接管理 =================
    def handle_tcp_connection(self, conn, addr):
        """处理TCP连接"""
        conn.settimeout(30)
        try:
            while self.running:
                try:
                    data = conn.recv(1024)
                    if not data:
                        break
                    self.display_message(f"[{addr[0]}] {data.decode()}")
                except socket.timeout:
                    conn.sendall(b'<HEARTBEAT>')
        except:
            pass
        finally:
            self.remove_connection(addr)

    def remove_connection(self, addr):
        """移除失效连接"""
        with self.lock:
            if addr in self.connections:
                try:
                    self.connections[addr].close()
                except:
                    pass
                del self.connections[addr]
            self.display_message(f"连接丢失: {addr[0]}:{addr[1]}")

    def start_connection_manager(self):
        """连接状态维护"""

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
        """检查连接状态"""
        try:
            conn.send(b'')
            return False
        except:
            return True

    # ================= 实用工具方法 =================
    def generate_subnet_ips(self, local_ips):
        """生成子网IP列表"""
        ips = []
        for ip in local_ips:
            if ip.startswith("127."):
                continue
            octets = ip.split('.')[:3]
            base_ip = '.'.join(octets) + '.'
            ips.extend(f"{base_ip}{i}" for i in range(1, 255))
        return list(set(ips))

    def get_local_ips(self):
        """获取本地IP地址"""
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
        """更新节点信息"""
        self.known_nodes[ip] = time.time()
        self.attempt_connect(ip, port)

    # ================= GUI相关方法 =================
    def display_message(self, message):
        """显示聊天消息"""
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, f"{time.strftime('%H:%M:%S')} {message}\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

    def send_message(self):
        """发送消息"""
        message = self.input_entry.get()
        if not message:
            return

        self.input_entry.delete(0, tk.END)
        self.display_message(f"我: {message}")

        with self.lock:
            dead_conns = []
            for addr, conn in self.connections.items():
                try:
                    conn.sendall(message.encode())
                except:
                    dead_conns.append(addr)

            for addr in dead_conns:
                self.remove_connection(addr)

    def gui_updater(self):
        """更新GUI状态"""
        with self.lock:
            # 清理节点列表
            for item in self.node_list.get_children():
                self.node_list.delete(item)

            # 添加活动连接（显示端口）
            for addr in self.connections:
                self.node_list.insert('', 'end', values=(f"{addr[0]}:{addr[1]}", "已连接"))

            # 添加已知节点（仅显示IP）
            for ip in self.known_nodes:
                if time.time() - self.known_nodes[ip] < 60:
                    self.node_list.insert('', 'end', values=(ip, "最近发现"))

        self.root.after(1000, self.gui_updater)

    def on_closing(self):
        """关闭程序处理"""
        if messagebox.askokcancel("退出", "确定要退出吗？"):
            self.running = False
            try:
                self.udp_socket.close()
                self.tcp_socket.close()
                for conn in self.connections.values():
                    conn.close()
            except:
                pass
            self.root.destroy()
            sys.exit(0)

    # ================= 新增功能方法 =================
    def show_ip_dialog(self):
        """显示IP输入对话框"""
        dialog = tk.Toplevel(self.root)
        dialog.title("选择扫描网段")
        dialog.geometry("300x100")

        ttk.Label(dialog, text="输入IP网段（如192.168.1）:").pack(pady=5)
        ip_entry = ttk.Entry(dialog)
        ip_entry.pack(pady=5)

        def do_scan():
            base_ip = ip_entry.get()
            if self.validate_ip(base_ip):
                dialog.destroy()
                threading.Thread(target=self.manual_scan, args=(base_ip,)).start()
            else:
                messagebox.showerror("错误", "无效的IP格式")

        ttk.Button(dialog, text="开始扫描", command=do_scan).pack()

    def validate_ip(self, ip_str):
        """验证IP网段格式"""
        parts = ip_str.split('.')
        if len(parts) != 3:
            return False
        return all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)

    def manual_scan(self, base_ip):
        """手动扫描指定网段"""
        self.manual_scanning = True
        try:
            ips = [f"{base_ip}.{i}" for i in range(1, 255)]
            for ip in ips:
                self.attempt_connect(ip, self.base_port)
                self.attempt_connect(ip, self.broadcast_port)
                time.sleep(0.01)  # 防止过于激进
        finally:
            self.manual_scanning = False

    def show_about(self):
        """显示关于信息"""
        about_msg = "HSHMENG P2P Chat\n版本 hshmeng_tools 8.1\n作者：HSHMENG"
        messagebox.showinfo("关于", about_msg)

def the_main():
    app = P2PChatAuto()
    app.root.mainloop()

if __name__ == "__main__":
    app = P2PChatAuto()
    app.root.mainloop()