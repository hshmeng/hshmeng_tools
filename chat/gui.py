import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time
import threading

class ChatGUI:
    def __init__(self, root, network_manager):
        self.root = root
        self.network_manager = network_manager
        self.root.title("HSHMENG Chat")
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.create_widgets()

        # 设置回调函数，用于将消息从NetworkManager传递到GUI
        self.network_manager.set_display_message_callback(self.display_message)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        online_frame = ttk.LabelFrame(main_frame, text="活跃节点")
        online_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        self.node_list = ttk.Treeview(online_frame, columns=('ip', 'status'), show='headings')
        self.node_list.heading('ip', text='IP地址')
        self.node_list.heading('status', text='状态')
        self.node_list.pack(fill=tk.BOTH, expand=True)

        button_frame = ttk.Frame(online_frame)
        button_frame.pack(fill=tk.X, pady=5)

        ttk.Button(button_frame, text="选择IP", command=self.show_ip_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="关于", command=self.show_about).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="退出", command=self.on_closing).pack(side=tk.RIGHT, padx=2)

        chat_frame = ttk.LabelFrame(main_frame, text="消息")
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.chat_area = scrolledtext.ScrolledText(chat_frame, wrap=tk.WORD, state='disabled')
        self.chat_area.pack(fill=tk.BOTH, expand=True)

        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)

        self.input_entry = ttk.Entry(input_frame)
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.input_entry.bind("<Return>", lambda e: self.send_message())

        ttk.Button(input_frame, text="发送", command=self.send_message).pack(side=tk.RIGHT)

    def display_message(self, message):
        self.chat_area.configure(state='normal')
        self.chat_area.insert(tk.END, f"{time.strftime('%H:%M:%S')} {message}\n")
        self.chat_area.configure(state='disabled')
        self.chat_area.see(tk.END)

    def send_message(self):
        message = self.input_entry.get()
        if not message:
            return

        self.input_entry.delete(0, tk.END)
        self.display_message(f"我: {message}")

        with self.network_manager.lock:
            dead_conns = []
            for addr, conn in self.network_manager.connections.items():
                try:
                    conn.sendall(message.encode())
                except:
                    dead_conns.append(addr)

            for addr in dead_conns:
                self.network_manager.remove_connection(addr)

    def gui_updater(self):
        with self.network_manager.lock:
            for item in self.node_list.get_children():
                self.node_list.delete(item)

            for addr in self.network_manager.connections:
                self.node_list.insert('', 'end', values=(f"{addr[0]}:{addr[1]}", "已连接"))

            for ip in self.network_manager.known_nodes:
                if time.time() - self.network_manager.known_nodes[ip] < 60:
                    self.node_list.insert('', 'end', values=(ip, "最近发现"))

        self.root.after(1000, self.gui_updater)

    def on_closing(self):
        if messagebox.askokcancel("退出", "确定要退出吗？"):
            self.network_manager.running = False
            try:
                self.network_manager.udp_socket.close()
                self.network_manager.tcp_socket.close()
                for conn in self.network_manager.connections.values():
                    conn.close()
            except:
                pass
            self.root.destroy()

    def show_ip_dialog(self):
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
                threading.Thread(target=self.network_manager.manual_scan, args=(base_ip,)).start()
            else:
                messagebox.showerror("错误", "无效的IP格式")

        ttk.Button(dialog, text="开始扫描", command=do_scan).pack()

    def validate_ip(self, ip_str):
        parts = ip_str.split('.')
        if len(parts) != 3:
            return False
        return all(part.isdigit() and 0 <= int(part) <= 255 for part in parts)

    def show_about(self):
        about_msg = "HSHMENG P2P Chat\n版本 hshmeng_tools 8.1\n作者：HSHMENG"
        messagebox.showinfo("关于", about_msg)