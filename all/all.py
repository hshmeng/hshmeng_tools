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

def random_jump(target_word):
    max_attempts = 3# 最大尝试次数
    def random_char():
        # 生成随机汉字（Unicode 范围：0x4E00 到 0x9FFF）
        return chr(random.randint(0x4E00, 0x9FFF))
    current_word = [" "] * len(target_word)
    for i in range(len(target_word)):
        attempts = 0
        while current_word[i] != target_word[i]:
            clear_console()
            if attempts < max_attempts:
                current_word[i] = random_char()
                attempts += 1
            else:
                current_word[i] = target_word[i]
            print("".join(current_word))