import ctypes

def rgb(r, g, b, text):
    return f"\033[38;2;{r};{g};{b}m{text}\033[0m"

def rgb_len(n, text):
    if n == 1:
        return f"\033[38;2;0;255;0m{text}\033[0m"
    if n == 2:
        return f"\033[38;2;0;255;255m{text}\033[0m"
    if n == 3:
        return f"\033[38;2;255;0;255m{text}\033[0m"
    else:
        return text

def page_1():
    # 运行模式检测
    def is_admin():
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False
    if is_admin():
        print(rgb(255, 255, 0, "当前是管理员模式运行！能够正常使用所有功能"))
    else:
        print(rgb(255, 255, 0, "当前非管理员模式运行，建议以管理员模式下运行"))
    print(rgb(0, 255, 0, "=====请选择一个选项（键入数字）v4.9====="))
    print(rgb_len(1, "1. [植物大战僵尸工具]"))
    print(rgb_len(2, "2. [极域电子教室工具]"))
    print(rgb_len(3, "3. [扫活工具]"))


def page_2(page):
    if page == "1":
        print(rgb_len(1, "1. 导入全解锁存档（目前为：v2.6.1存档）"))
        print(rgb_len(1, "2. 将当前游戏存档备份"))
        print(rgb_len(1, "3. 打开当前游戏存档目录"))
        print(rgb_len(1, "4. 存档自动备份（需要输入备份间隔时间）"))
    elif page == "2":
        print(rgb_len(2, "1. 极域电子教室工具（JiYuTrainer.exe）"))
        print(rgb_len(2, "2. 极域电子教室工具快捷键教学"))
        print(rgb_len(2, "3. 极域电子教室一键杀死（TK极域bat）"))
    elif page == "3":
        print(rgb_len(3, "1. 扫描指定ip地址的端口号"))
        print(rgb_len(3, "2. 常见端口及其服务内容"))
        print(rgb_len(3, "3. 扫描指定ip地址网段存活主机"))
        print(rgb_len(3, "4. 扫描所有开启共享文件夹的ip地址"))


def pege_warning():
    print(rgb(0, 255, 0, "exit. 退出程序"))
    print(rgb(255, 0, 0, "此程序可以后台运行，按住键盘上Alt+Q组合键，自动关闭植物大战僵尸程序和本程序"))
    print(rgb(255, 0, 0, "自动关闭后，游戏进度不会消失，请放心使用（进度丢了没有售后）"))
