import os, random

def clear_console():
    # 对于Windows系统
    if os.name == 'nt':
        os.system('cls')
    # 对于Unix/Linux/Mac系统
    else:
        os.system('clear')

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
