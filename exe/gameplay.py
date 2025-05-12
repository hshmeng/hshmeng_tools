import random
import time


def guess_number_game():
    print("欢迎来到猜数字游戏！\n游戏玩法：我会随机生成一个数字，你需要在指定范围内猜测这个数字。")
    min_num = 0
    max_num = 100000000

    # 获取用户输入的范围
    try:
        user_min = int(input(f"请输入最小值（默认{min_num}）：") or min_num)
        user_max = int(input(f"请输入最大值（默认{max_num}）：") or max_num)

        if user_min >= user_max:
            print("最小值必须小于最大值，将使用默认范围。")
        else:
            min_num, max_num = user_min, user_max
    except ValueError:
        print("输入无效，将使用默认范围。")

    # 生成随机数
    target = random.randint(min_num, max_num)
    attempts = 0
    start_time = time.time()

    print(f"\n我已经想好了一个{min_num}到{max_num}之间的数字，开始猜吧！")

    # 游戏主循环
    while True:
        try:
            guess = int(input("你的猜测是："))
            attempts += 1

            if guess < target:
                print("太小了！")
            elif guess > target:
                print("太大了！")
            else:
                end_time = time.time()
                time_used = round(end_time - start_time, 2)
                input(f"\n恭喜你！你用了{attempts}次猜测，在{time_used}秒内猜中了数字{target}！回车退出游戏。")
                break
        except ValueError:
            print("请输入一个有效的整数！")



def number_position_game():
    print("欢迎来到数字位置猜谜游戏！")
    print("你需要猜测一组不重复的数字，我会告诉你数字对和位置对的数量。")

    # 获取用户想要的数字个数
    while True:
        try:
            num_count = int(input("请选择要猜的数字个数(2-10): "))
            if 2 <= num_count <= 10:
                break
            else:
                print("请输入2-10之间的数字！")
        except ValueError:
            print("请输入有效的数字！")

    # 生成随机数字组合
    digits = list("1234567890")
    random.shuffle(digits)
    target = digits[:num_count]
    target_str = ''.join(target)

    attempts = 0
    start_time = time.time()

    print(f"\n我已经想好了一个{num_count}位不重复的数字组合，开始猜吧！")

    # 游戏主循环
    while True:
        guess = input(f"请输入你的猜测({num_count}位不重复数字): ")
        attempts += 1

        # 验证输入
        if len(guess) != num_count or not guess.isdigit() or len(set(guess)) != num_count:
            print(f"请输入{num_count}位不重复的数字！")
            continue

        # 计算数字对和位置对
        correct_digits = 0
        correct_positions = 0

        for i in range(num_count):
            if guess[i] in target:
                correct_digits += 1
            if guess[i] == target[i]:
                correct_positions += 1

        # 反馈结果
        print(f"结果: 数字对 {correct_digits}个, 位置对 {correct_positions}个")

        # 检查是否猜中
        if correct_positions == num_count:
            end_time = time.time()
            time_used = round(end_time - start_time, 2)
            input(f"\n恭喜你！你用了{attempts}次尝试，在{time_used}秒内猜中了数字组合 {target_str}！")
            break

