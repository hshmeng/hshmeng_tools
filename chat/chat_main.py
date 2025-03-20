import socket
import threading
import sys
import time
from queue import Queue
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox


class P2PChatGUI:
    def __init__(self, port=8070):
        self.port = port
        self.connections = []
        self.running = True
        self.lock = threading.Lock()
        self.server_socket = None
        self.local_ips = self.get_all_local_ips()
        self.scan_queue = Queue()
        self.scan_threads = []
        self.scan_interval = 30

        # GUI初始化
        self.root = tk.Tk()
        self.root.title(f"P2P聊天室 - 本机IP: {', '.join(self.local_ips)}")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        # 创建界面布局
        self.create_widgets()

        # 启动后台服务
        self.start_server()
        self.start_network_scanner()

        # 启动GUI更新线程
        self.gui_update()

    def get_all_local_ips(self):
        ips = []
        try:
            # 获取所有网络接口的IP地址
            host_name = socket.gethostname()
            host_info = socket.gethostbyname_ex(host_name)[2]
            for ip in host_info:
                if not ip.startswith("127."):
                    ips.append(ip)
        except:
            pass
        return ips if ips else ["127.0.0.1"]

    def generate_subnet_ips(self):
        all_ips = []
        for ip in self.local_ips:
            if ip.startswith("127."):
                continue
            octets = ip.split('.')[:3]
            base_ip = '.'.join(octets) + '.'
            subnet_ips = [base_ip + str(i) for i in range(1, 255) if base_ip + str(i) not in self.local_ips]
            all_ips.extend(subnet_ips)
        return list(set(all_ips))

    def create_widgets(self):
        # 主框架布局
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 上半部分：在线列表和功能按钮
        top_frame = ttk.Frame(main_frame)
        top_frame.pack(fill=tk.BOTH, expand=True)

        # 在线列表 (左)
        online_frame = ttk.LabelFrame(top_frame, text="在线节点")
        online_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        self.online_list = tk.Listbox(online_frame)
        self.online_list.pack(fill=tk.BOTH, expand=True)

        # 功能按钮 (右)
        button_frame = ttk.Frame(top_frame)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=5)

        ttk.Button(button_frame, text="退出", command=self.on_closing).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="清空聊天").pack(fill=tk.X, pady=2)  # 占位符
        ttk.Button(button_frame, text="设置").pack(fill=tk.X, pady=2)  # 占位符
        ttk.Button(button_frame, text="关于").pack(fill=tk.X, pady=2)  # 占位符

        # 聊天内容显示
        chat_frame = ttk.LabelFrame(main_frame, text="聊天内容")
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        self.chat_area = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, state='disabled')
        self.chat_area.pack(fill=tk.BOTH, expand=True)

        # 输入区域
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)

        self.input_entry = ttk.Entry(input_frame)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_entry.bind("<Return>", lambda e: self.send_message())

        ttk.Button(input_frame, text="发送", command=self.send_message).pack(side=tk.RIGHT)

    def gui_update(self):
        # 更新在线列表
        with self.lock:
            online_ips = set()
            for conn in self.connections:
                try:
                    online_ips.add(conn.getpeername()[0])
                except:
                    pass

            current_list = self.online_list.get(0, tk.END)
            new_ips = list(online_ips)

            # 删除不在线的
            for ip in current_list:
                if ip not in new_ips:
                    self.online_list.delete(current_list.index(ip))

            # 添加新的在线IP
            for ip in new_ips:
                if ip not in current_list:
                    self.online_list.insert(tk.END, ip)

        # 每1秒更新一次
        self.root.after(1000, self.gui_update)

    def start_server(self):
        def server_thread():
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind(('0.0.0.0', self.port))
            self.server_socket.listen(5)

            while self.running:
                try:
                    conn, addr = self.server_socket.accept()
                    with self.lock:
                        self.connections.append(conn)
                    threading.Thread(target=self.handle_client, args=(conn, addr)).start()
                    self.append_message(f"新连接来自 {addr[0]}")
                except:
                    break

        threading.Thread(target=server_thread, daemon=True).start()

    def handle_client(self, conn, addr):
        try:
            while self.running:
                data = conn.recv(1024)
                if not data:
                    break
                message = data.decode()
                self.append_message(f"来自 {addr[0]}: {message}")
        except:
            pass
        finally:
            with self.lock:
                if conn in self.connections:
                    self.connections.remove(conn)
            conn.close()
            self.append_message(f"{addr[0]} 已断开连接")

    def start_network_scanner(self):
        def scan_worker():
            while self.running:
                ip = self.scan_queue.get()
                if ip is None:
                    break
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.settimeout(1)
                        s.connect((ip, self.port))
                        with self.lock:
                            existing_ips = [conn.getpeername()[0] for conn in self.connections if conn._closed == False]
                            if ip not in existing_ips:
                                self.connect_to_peer(ip)
                except:
                    pass
                finally:
                    self.scan_queue.task_done()

        # 启动扫描线程池
        for _ in range(20):
            t = threading.Thread(target=scan_worker)
            t.daemon = True
            t.start()
            self.scan_threads.append(t)

        # 定期扫描
        def scanner():
            while self.running:
                self.scan_queue.join()  # 等待上次扫描完成
                ips = self.generate_subnet_ips()
                for ip in ips:
                    self.scan_queue.put(ip)
                time.sleep(self.scan_interval)

        threading.Thread(target=scanner, daemon=True).start()

    def connect_to_peer(self, ip):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((ip, self.port))
            with self.lock:
                self.connections.append(sock)
            threading.Thread(target=self.handle_client, args=(sock, (ip, self.port))).start()
            self.append_message(f"已连接到 {ip}")
        except Exception as e:
            pass

    def send_message(self):
        message = self.input_entry.get()
        if not message:
            return

        self.input_entry.delete(0, tk.END)
        self.append_message(f"我: {message}")

        with self.lock:
            to_remove = []
            for conn in self.connections:
                try:
                    conn.sendall(message.encode())
                except:
                    to_remove.append(conn)

            for conn in to_remove:
                self.connections.remove(conn)

    def append_message(self, message):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, f"{time.strftime('%H:%M:%S')} {message}\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

    def on_closing(self):
        if messagebox.askokcancel("退出", "确定要退出程序吗？"):
            self.running = False
            with self.lock:
                for conn in self.connections:
                    try:
                        conn.close()
                    except:
                        pass
                self.connections = []
            if self.server_socket:
                self.server_socket.close()
            self.root.destroy()
            sys.exit(0)


if __name__ == "__main__":
    app = P2PChatGUI()
    app.root.mainloop()