import ctypes, socket

def rgb(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def rgb_len(n, text):
    if n == "red":#255,0,0
        return f"\033[38;2;255;0;0m{text}\033[0m"
    if n == "green":#0,255,0
        return f"\033[38;2;0;255;0m{text}\033[0m"
    if n == "blue":#0,0,255
        return f"\033[38;2;0;0;255m{text}\033[0m"
    if n == "yellow":#255,255,0
        return f"\033[38;2;255;255;0m{text}\033[0m"
    if n == "purple":#255,0,255
        return f"\033[38;2;255;0;255m{text}\033[0m"
    if n == "Cyan":#0,255,255
        return f"\033[38;2;0;255;255m{text}\033[0m"
    else:
        return text

def get_ip_address():
    ip_list = []
    hostname = socket.gethostname()  # 获取本机所有IP地址
    ip_addresses = socket.gethostbyname_ex(hostname)[2]
    for ip in ip_addresses:# 打印所有IP地址
        ip_list.append(ip)
    print(rgb_len("yellow", f"当前电脑IP地址为：{ip_list}"))

def get_mac_address():
    hostname = socket.gethostname()
    print(rgb_len("yellow",  f"本机名称是: {hostname}"))

def page_1():
    # 运行模式检测
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    if is_admin():
        print(rgb_len("yellow", "当前是管理员模式运行！能够正常使用所有功能"))
    else:
        print(rgb_len("yellow", "当前非管理员模式运行，建议以管理员模式下运行"))

    get_ip_address()
    get_mac_address()
    print(rgb_len("purple", "=====请选择一个选项（键入数字）v5.3====="))
    print(rgb_len("green", "1. [植物大战僵尸工具]"))
    print(rgb_len("green", "2. [极域电子教室工具]"))
    print(rgb_len("green", "3. [扫活工具]"))
    print(rgb_len("green", "4. [共享操作]"))
    print(rgb_len("green", "5. [本机管理工具]"))



def page_2(page):
    if page == "1":
        print(rgb_len("green", "1. 【植物大战僵尸杂交版pvzHE】导入全解锁存档（目前为：v2.6.1存档）"))
        print(rgb_len("green", "2. 【植物大战僵尸杂交版pvzHE】将当前游戏存档备份"))
        print(rgb_len("green", "3. 【植物大战僵尸杂交版pvzHE】打开当前游戏存档目录"))
        print(rgb_len("green", "4. 【植物大战僵尸杂交版pvzHE】存档自动备份（需要输入备份间隔时间）"))
        print(rgb_len("green", "5. 【植物大战僵尸杂交版pvzHE】外挂程序一键启动（外挂版本：23.52）"))
        print(rgb_len("green", "6. 【植物大战僵尸威化版Weihua】导入全解锁存档"))
        print(rgb_len("green", "7. 【植物大战僵尸威化版Weihua】将当前游戏存档备份"))
        print(rgb_len("green", "8. 【植物大战僵尸威化版Weihua】打开存档目录"))
    elif page == "2":
        print(rgb_len("green", "1. 极域电子教室工具（JiYuTrainer.exe）"))
        print(rgb_len("green", "2. 极域电子教室工具快捷键教学"))
        print(rgb_len("green", "3. 极域电子教室一键杀死（TK极域bat）"))
    elif page == "3":
        print(rgb_len("green", "1. 扫描指定ip地址开放的端口号"))
        print(rgb_len("green", "2. 常见端口及其服务内容"))
        print(rgb_len("green", "3. 扫描指定ip地址网段存活主机"))
    elif page == "4":
        print(rgb_len("green", "1. 扫描所有开启共享文件夹的ip地址"))
        print(rgb_len("green", "2. 尝试一键把所有共享文件复制到D盘根目录下"))
        print(rgb_len("green", "3. 本机开放的共享文件夹"))
        print(rgb_len("green", "4. 尝试一键关闭本机所有共享文件夹"))
        print(rgb_len("green", "5. 备份所有共享文件夹目录"))
        print(rgb_len("green", "6. 开启所有备份的共享文件夹目录"))
    elif page == "5":
        print(rgb_len("green", "1. 设备规格"))
        print(rgb_len("green", "2. windows规格"))
        print(rgb_len("green", "3. 设备管理器"))


def pege_warning():
    print(rgb_len("Cyan", "exit. 退出程序"))
    print(rgb_len("Cyan", "author. 作者信息"))
    print(rgb_len("red", "此程序可以后台运行，按住键盘上Alt+Q组合键，自动关闭植物大战僵尸程序和本程序"))
    print(rgb_len("red", "自动关闭后，游戏进度不会消失，请放心使用（进度丢了没有售后）"))
