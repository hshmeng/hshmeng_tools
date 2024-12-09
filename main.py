import ctypes
import keyboard
import pygetwindow as gw
import win32gui
import win32con
from exes import *

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
v6.8更新内容：
NEW：新的分类“共享操作”
1.更新了 本机信息工具>设备规格
2.更新了 本机信息工具>windows规格
3.更新了 本机信息工具>设备管理器
4.更新了 共享操作>本机开放的共享文件夹
5.更新了 共享操作>尝试一键关闭本机所有共享文件夹
6.更新了 共享操作>备份所有共享文件夹目录
7.更新了 共享操作>开启所有备份的共享文件夹目录
8.修复了 共享操作>尝试一键关闭本机所有共享文件夹 会把关键配置删除的错误
""")

def main():
    page.page_1()
    page.pege_warning()
    pages = input(rgb(0, 255, 0, "1输入选项>>>"))
    def ys():
        exe_list = ["1", "2", "3", "4", "5"]
        if pages in exe_list:
            choice = input(rgb(0, 255, 0, "请输入选项>>>"))
        if pages == "1":
            exe_1(choice)
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
    ys()


    if pages == "exit":
        clear_console()
        print(random_jump("我们正在入侵你的电脑！！！\n感受恐惧吧！！！"))
        exit()
    if pages == "author":
        clear_console()
        author = """█░█ █▀ █░█ █▀▄▀█ █▀▀ █▄░█ █▀▀\n█▀█ ▄█ █▀█ █░▀░█ ██▄ █░▀█ █▄█"""
        print(rgb(0, 255, 0, author))
        input(rgb(0, 255, 0, "按回车键退出>>>"))

while True:
    main()


# pyinstaller -F -i qiqi.ico main.py