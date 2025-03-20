from network import NetworkManager
from gui import ChatGUI
import tkinter as tk
import random

def main():
    base_port = random.randint(9000, 9999)
    broadcast_port = 9099

    network_manager = NetworkManager(base_port, broadcast_port)
    network_manager.start_tcp_server()
    network_manager.start_udp_service()
    network_manager.start_scanner()
    network_manager.start_connection_manager()

    root = tk.Tk()
    root.iconbitmap('..\\qiqi.ico')
    app = ChatGUI(root, network_manager)
    app.gui_updater()
    root.mainloop()

if __name__ == "__main__":
    main()