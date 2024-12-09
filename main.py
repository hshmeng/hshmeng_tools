import ctypes
import keyboard
import pygetwindow as gw
import win32gui
import win32con
from exes import *

if_caidan = 0

def caidan():
    # 获取当前窗口的句柄
    hwnd = win32gui.GetForegroundWindow()

    # 定义按键序列检测函数
    def check_sequence(sequence, input_sequence):
        return sequence == input_sequence[-len(sequence):]

    # 处理按键事件的函数
    def handle_key_press():
        sequence = ['up', 'up', 'down', 'down', 'left', 'right', 'left', 'right']
        input_sequence = []

        while True:
            if ctypes.windll.user32.GetAsyncKeyState(win32con.VK_UP):
                input_sequence.append('up')
            elif ctypes.windll.user32.GetAsyncKeyState(win32con.VK_DOWN):
                input_sequence.append('down')
            elif ctypes.windll.user32.GetAsyncKeyState(win32con.VK_LEFT):
                input_sequence.append('left')
            elif ctypes.windll.user32.GetAsyncKeyState(win32con.VK_RIGHT):
                input_sequence.append('right')

            # 检查按键序列
            if check_sequence(sequence, input_sequence):
                if_caidan = 1
                print("列表似乎发生了变化")
                input_sequence = []  # 重置输入序列

            time.sleep(0.1)  # 添加延迟以避免高CPU使用率

    # 开始处理按键事件
    handle_key_press()

caidan()

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def close_window_by_title(title):
    windows = gw.getWindowsWithTitle(title)
    print(f"Found windows: {windows}")
    for window in windows:
        if title in window.title:
            hwnd = window._hWnd
            print(f"Closing window: {window.title} (HWND: {hwnd})")
            result = win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            print(f"PostMessage result: {result}")

def on_close_hotkey():
    close_window_by_title("植物大战僵尸")
    close_window_by_title("JiYu")
    # 退出脚本
    os._exit(0)

keyboard.add_hotkey('alt+q', on_close_hotkey)

# 刷新颜色
print(rgb(255, 0, 0, "键入回车进入程序>>>"))
clear_console()
c = input(rgb(255, 0, 0, "键入回车进入程序>>>"))

# ma_1()

print("""=====公告=====
原先的字体色彩过于丰富，不便于整理，故取消过于丰富的颜色
v7.0更新内容：
WARN:我们删除了“植物大战僵尸工具”
1. 更新了废弃的功能检索功能
2. 更新了一个彩蛋！彩蛋！彩蛋！彩蛋！彩蛋！（提示：最经典的作弊代码）
""")

def main():
    page.page_1()
    page.pege_warning()
    pages = input(rgb(0, 255, 0, "输入选项>>>"))
    def ys():
        exe_list = ["2", "3", "4", "5"]
        if pages in exe_list:
            choice = input(rgb(0, 255, 0, "请输入选项>>>"))
        if pages == "2":
            exe_2(choice)
        if pages == "3":
            exe_3(choice)
        if pages == "4":
            exe_4(choice)
        if pages == "5":
            exe_5(choice)
    clear_console()
    page.page_2(pages)
    if if_caidan == 1:
        print(rgb_len("Cyan", "【彩蛋】李猛烧香（输入：李猛烧香，体验彩蛋）"))
    ys()
    if pages == "exit":
        clear_console()
        print(random_jump("我们正在入侵你的电脑！！！\n感受恐惧吧！！！"))
        exit()
    if pages == "author":
        clear_console()
        author = """█░█ █▀ █░█ █▀▄▀█ █▀▀ █▄░█ █▀▀\n█▀█ ▄█ █▀█ █░▀░█ ██▄ █░▀█ █▄█"""
        print(rgb_len("green", author))
        input(rgb_len("green", "按回车键退出>>>"))
    if pages == "del":
        clear_console()
        print(rgb_len("green", "废弃的功能："))
        print(rgb_len("purple", "【植物大战僵尸杂交版pvzHE】导入全解锁存档（目前为：v2.6.1存档）"),rgb_len("red","存在版本：v3_1 v4_5 v4_9 v5_4 v6_0 v6_6 v6_7 v6_8"))
        print(rgb_len("purple", "【植物大战僵尸杂交版pvzHE】将当前游戏存档备份"),rgb_len("red", "存在版本：v3_1 v4_5 v4_9 v5_4 v6_0 v6_6 v6_7 v6_8"))
        print(rgb_len("purple", "【植物大战僵尸杂交版pvzHE】打开当前游戏存档目录"),rgb_len("red", "存在版本：v3_1 v4_5 v4_9 v5_4 v6_0 v6_6 v6_7 v6_8"))
        print(rgb_len("purple", "【植物大战僵尸杂交版pvzHE】存档自动备份（需要输入备份间隔时间）"),rgb_len("red", "存在版本：v3_1 v4_5 v4_9 v5_4 v6_0 v6_6 v6_7 v6_8"))
        print(rgb_len("purple", "【植物大战僵尸杂交版pvzHE】外挂程序一键启动（外挂版本：23.52）"),rgb_len("red", "存在版本：v6_0 v6_6 v6_7 v6_8"))
        print(rgb_len("purple", "【植物大战僵尸威化版Weihua】导入全解锁存档"),rgb_len("red", "存在版本：v6_0 v6_6 v6_7 v6_8"))
        print(rgb_len("purple", "【植物大战僵尸威化版Weihua】将当前游戏存档备份"),rgb_len("red", "存在版本：v6_0 v6_6 v6_7 v6_8"))
        print(rgb_len("purple", "【植物大战僵尸威化版Weihua】打开存档目录"),rgb_len("red", "存在版本：v6_0 v6_6 v6_7 v6_8"))
    if pages == "李猛烧香":
        for _ in range(3):
            print(rgb_len("red", "警告！！！你确定要执行李猛烧香吗！！！该操作不可逆转！！！（此功能不会对电脑造成危害，但是会让电脑变的很智）"))


while True:
    main()


# pyinstaller -F -i qiqi.ico main.py