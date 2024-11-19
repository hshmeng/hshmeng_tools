import shutil, datetime, time, subprocess
import platform
import socket
from concurrent.futures import ThreadPoolExecutor

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
        clear_console()

        def get_local_ip_addresses():
            # 获取当前机器的所有本地IP地址
            hostname = socket.gethostname()
            local_ips = socket.gethostbyname_ex(hostname)[2]
            return local_ips

        def ping(host):
            # 返回True如果主机响应ping请求
            param = '-n' if platform.system().lower() == 'windows' else '-c'
            command = ['ping', param, '1', host]
            return subprocess.call(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0

        def scan_ip(ip):
            # 扫描单个IP地址
            if ping(ip):
                return ip
            return None

        def scan_network(network_prefix):
            # 使用多线程扫描网络中的活动主机
            active_hosts = []
            with ThreadPoolExecutor(max_workers=100) as executor:
                futures = [executor.submit(scan_ip, f"{network_prefix}.{i}") for i in range(1, 255)]
                for future in futures:
                    result = future.result()
                    if result:
                        active_hosts.append(result)
            return active_hosts

        # 获取所有本地IP地址
        local_ips = get_local_ip_addresses()

        # 显示本地IP地址并让用户选择网络前缀
        print("找到的本地IP地址:")
        for idx, ip in enumerate(local_ips):
            print(f"{idx}. {ip}")

        # 由于当前环境不支持用户输入，请手动选择一个IP地址
        # 例如，选择第一个IP地址
        lis = int(input("请输入希望扫描的网段>>>"))
        selected_ip = local_ips[lis]
        network_prefix = '.'.join(selected_ip.split('.')[:-1])

        # 扫描选定的网络前缀
        active_hosts = scan_network(network_prefix)

        print(f"网络 {network_prefix}.x 中的活动主机:")
        for host in active_hosts:
            print(host)
