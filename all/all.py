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