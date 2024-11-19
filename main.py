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

def emoticons():
    emoticons1 = """┬┴┬┌─  ●─┬─  │ ─┼─┐  ●├─┤○\n┴┬┴├┬  ┌─┼─  │◎ │ │  ○└┬┘●\n─┼─││  │ │  ││ ─┴─┴  ──┼──\n●│○││  ┴─┼─  │ ○  ●  ／│＼"""
    emoticons2 = """█░█ █▀ █░█ █▀▄▀█ █▀▀ █▄░█ █▀▀\n█▀█ ▄█ █▀█ █░▀░█ ██▄ █░▀█ █▄█"""
    emoticons3 = """█   █░░ █▀█ █░█ █▀▀   █▄█ █▀█ █░█\n█   █▄▄ █▄█ ▀▄▀ ██▄   ░█░ █▄█ █▄█"""
    emoticons_list = [emoticons1, emoticons2, emoticons3]
    selected_emoticon = random.choice(emoticons_list)
    print()
    print(rgb(0, 255, 0, selected_emoticon))
    print()


# 刷新颜色
print(rgb(255, 0, 0, "键入回车进入程序>>>"))
clear_console()
# 刷新完成，一个小emoji
emoticons()
input(rgb(255, 0, 0, "键入回车进入程序>>>"))
clear_console()

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
        print("没有做")
    if pages == "exit":
        clear_console()
        print(random_jump("我们正在入侵你的电脑！！！\n感受恐惧吧！！！"))
        exit()

while True:
    main()

