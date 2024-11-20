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
if c == "123":
    pass
else:
    ma_1()

print("""=====公告=====
原先的字体色彩过于丰富，不便于整理，故取消过于丰富的颜色
v5.3更新内容：
1. 上方显示电脑ip地址，本机名称
2. 扫活工具新增一个功能
3. 取消开屏小广告
4. 增加作者信息栏目""")

def main():
    page.page_1()
    page.pege_warning()
    pages = input(rgb(0, 255, 0, "请输入选项>>>"))

    clear_console()
    if pages == "1":
        clear_console()
        page.page_2(pages)
        choice = input(rgb(0, 255, 0, "请输入选项>>>"))
        exe_1(choice)
    if pages == "2":
        clear_console()
        page.page_2(pages)
        choice = input(rgb(0, 255, 0, "请输入选项>>>"))
        exe_2(choice)
    if pages == "3":
        clear_console()
        page.page_2(pages)
        choice = input(rgb(0, 255, 0, "请输入选项>>>"))
        exe_3(choice)
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