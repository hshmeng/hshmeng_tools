import shutil, datetime, time, subprocess, ipaddress, threading, socket
from scapy.all import *
from smbprotocol.connection import Connection
from smbprotocol.session import Session
from smbprotocol.tree import TreeConnect
from smbprotocol.open import Open

from all import *
from exe import jiyu, files, page

def exe_1(choice):
    # C:\ProgramData\PopCap Games\PlantsVsZombies\pvzHE\yourdata
    source_dir = os.path.join(os.getcwd(), 'hshmeng')
    target_dir = r'C:\\ProgramData\\PopCap Games\\PlantsVsZombies\\pvzHE\\yourdata'

    # 确保目标目录存在
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    if choice == "1":
        # 复制hshmeng文件夹及其子文件夹和文件
        if input(rgb(255, 0, 0, "此操作不可逆！是否确定！您可以先手动2选项备份！（确定请输入y）")) == 'y':
            clear_console()
            # 确保目标目录存在
            os.makedirs(target_dir, exist_ok=True)
            # 复制文件
            try:
                files.get_users_dat()
                print(rgb(255, 0, 0, "成功导入全解锁存档！！！"))
            except:
                print(rgb(255, 0, 0, "导入全解锁存档失败！！！"))
        else:
            clear_console()
            print(rgb(255, 0, 0, "注意！操作已取消。"))
    elif choice == "2":
        # 创建以当前时间命名的文件夹
        timestamp = datetime.datetime.now().strftime("%Y年%m月%d日_%H时%M分%S秒%f毫秒")
        timestamp = timestamp.replace(":", "_").replace("/", "_").replace("\\", "_").replace(" ", "0")
        new_dir = os.path.join(os.getcwd(), timestamp)
        os.makedirs(new_dir)
        # 复制目标目录的文件到当前目录
        shutil.copytree(target_dir, new_dir, dirs_exist_ok=True)
        clear_console()
        print(f"目标目录的所有文件已复制到当前目录下的 {new_dir} 文件夹！")
    elif choice == "3":
        # 打开存档目录
        os.startfile(target_dir)
        clear_console()
        print(f"已打开存档目录：{target_dir}")
    elif choice == "4":
        # 自动备份功能
        clear_console()
        print(rgb(255, 0, 0, "注意！启用此功能后，其它功能无法使用，只能通过关闭程序取消备份"))
        print(rgb(255, 0, 0, "不会影响Alt+Q快捷关闭功能"))
        if input(rgb(255, 0, 0, "是否确认开启功能请输入（确定请输入y）>>>")) == 'y':
            interval = int(input(rgb(255, 0, 0, "请输入备份间隔时间（秒）>>>")))
            clear_console()
            print(rgb(0, 255, 0, f"自动备份已启动，每 {interval} 秒备份一次。"))
            try:
                while True:
                    timestamp = datetime.datetime.now().strftime("%Y年%m月%d日_%H时%M分%S秒%f毫秒")
                    timestamp = timestamp.replace(":", "_").replace("/", "_").replace("\\", "_").replace(" ", "0")
                    new_dir = os.path.join(os.getcwd(), timestamp)
                    os.makedirs(new_dir)
                    shutil.copytree(target_dir, new_dir, dirs_exist_ok=True)
                    print(f"备份完成：{new_dir}")
                    time.sleep(interval)
            except KeyboardInterrupt:
                clear_console()
                print(rgb(255, 0, 0, "自动备份已停止。"))
        else:
            clear_console()
            print(rgb(255, 0, 0, f"已经取消自动备份"))
    else:
        clear_console()
        print(rgb(255, 0, 0, "请输入正确的选项！"))

def exe_2(choice):
    if choice == "1":
        clear_console()
        # 尝试复制到 C 盘根目录
        try:
            print(rgb(255, 0, 0, "正在尝试创建到C盘根目录下>>>"), end="")
            jiyu.run_exe("C:/JiYuTrainer.exe")
            # 运行临时文件
            subprocess.run(['C:/JiYuTrainer.exe'])
        except (PermissionError, FileNotFoundError):
            # 如果复制到 C 盘根目录失败，尝试复制到 D 盘根目录
            print(rgb(255, 0, 0, "失败"))
            print(rgb(255, 0, 0, "正在尝试创建到D盘根目录下>>>"), end="")
            try:
                print()
                jiyu.run_exe("D:/JiYuTrainer.exe")
                # 运行临时文件
                subprocess.run(['D:/JiYuTrainer.exe'])
            except (PermissionError, FileNotFoundError):
                print(rgb(255, 0, 0, "失败"))
                for i in range(3):
                    print(rgb(255, 0, 0, "我们没有任何权限！！！尝试以管理员身份运行！！！"))
    elif choice == "2":
        clear_console()
        print(rgb(255, 0, 0, "Ctrl + Alt + F: 紧急全屏快捷键"))
        print(rgb(255, 0, 0, "Ctrl + Alt + D: 快速显示/隐藏窗口快捷键"))
    elif choice == "3":
        clear_console()
        # 尝试复制到 C 盘根目录
        try:
            print(rgb(255, 0, 0, "正在尝试创建到C盘根目录下>>>"), end="")
            jiyu.tk_jy("C:/TK.bat")
            # 运行临时文件
            subprocess.run(['C:/TK.bat'])
        except (PermissionError, FileNotFoundError):
            # 如果复制到 C 盘根目录失败，尝试复制到 D 盘根目录
            print(rgb(255, 0, 0, "失败"))
            print(rgb(255, 0, 0, "正在尝试创建到D盘根目录下>>>"), end="")
            try:
                print()
                jiyu.tk_jy("D:/TK.bat")
                # 运行临时文件
                subprocess.run(['D:/TK.bat'])
            except (PermissionError, FileNotFoundError):
                print(rgb(255, 0, 0, "失败"))
                for i in range(3):
                    print(rgb(255, 0, 0, "我们没有任何权限！！！尝试以管理员身份运行！！！"))
    else:
        clear_console()
        print(rgb(255, 0, 0, "请输入正确的选项！"))

def exe_3(choice):
    if choice == "1":
        def scan(ip, port):# 定义扫描函数
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(rgb(255, 0, 0, f"端口{port}开放在{ip}上"))
            sock.close()
        def thread_scan(ip, ports):# 多线程扫描函数
            threads = []
            for port in ports:
                t = threading.Thread(target=scan, args=(ip, port))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()
        try:# 获取用户输入
            print(rgb(255, 255, 0, "退出这个功能只需要不写入数据即可"))
            ip_address = input(rgb(255, 0, 0,"请输入要扫描的IP地址："))
            ports_list = input(rgb(255, 0, 0, "1.扫描所有端口（很慢）\n2.扫描常用端口（较快）\n3.扫描指定端口（多个之间使用;分割）\n请选择："))
            clear_console()
            if ports_list == "1":
                ports = range(0, 65535 + 1)
                thread_scan(ip_address, ports)
            elif ports_list == "2":
                ports = [20, 21, 22, 23, 25, 53, 67, 68, 80, 110, 143, 443, 445, 3389, 8000, 8080]
                thread_scan(ip_address, ports)
            elif ports_list == "3":
                ports = input(rgb(255, 0, 0,"请输入要扫描的端口：")).split(";")
                ports = [int(port) for port in ports]
                print(ports)
                thread_scan(ip_address, ports)
        except Exception as e:
            clear_console()
            print(rgb(255, 0, 0,"出现错误或者人为希望退出这个程序"))
    elif choice == "2":
        clear_console()
        print(rgb(255, 0, 0, files.get_port_info()))
    elif choice == "3":
        clear_console()
        def ping(ip):# 定义扫描函数
            result = subprocess.run(['ping', '-n', '1', '-w', '1000', str(ip)], capture_output=True, text=True)
            if "TTL=" in result.stdout:
                print(rgb(255, 0, 0, f"{ip} 存活"))
        def thread_scan(network):# 多线程扫描函数
            threads = []
            for ip in network:
                t = threading.Thread(target=ping, args=(ip,))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
        try:# 获取用户输入
            network_input = input(rgb(255, 0, 0, "请输入要扫描的网段（例如：192.168.1.0/24）："))
            clear_console()
            network = ipaddress.ip_network(network_input, strict=False)
            thread_scan(network)
        except Exception as e:
            print(rgb(255, 0, 0, f"出现错误！！！请确认是否有写错！！！"))
    elif choice == "4":
        clear_console()
        def scan_shared_folders(ip):# 定义扫描函数
            try:
                connection = Connection(uuid.uuid4(), str(ip))
                connection.connect()
                session = Session(connection, "guest", "")
                session.connect()
                print(rgb(255, 0, 0, f"{ip} 开启了共享文件夹"))
            except Exception as e:
                pass
        def thread_scan(network):# 多线程扫描函数
            threads = []
            for ip in network:
                t = threading.Thread(target=scan_shared_folders, args=(ip,))
                threads.append(t)
                t.start()

            for t in threads:
                t.join()
        try:# 获取用户输入
            network_input = input(rgb(255, 0, 0, "请输入要扫描的网段（例如：192.168.1.0/24）："))
            clear_console()
            network = ipaddress.ip_network(network_input, strict=False)
            thread_scan(network)
        except Exception as e:
            print(rgb(255, 0, 0, "扫描出错！！！"))
    else:
        clear_console()
        print(rgb(255, 0, 0, "请输入正确的选项！"))
