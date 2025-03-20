import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import math


class LotteryWheel:
    def __init__(self, root):
        self.root = root
        self.root.title("抽奖圆盘")
        self.root.geometry("500x550")  # 设置初始窗口大小

        # 上方画布
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # 底部按钮栏
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=5)

        self.items = []
        self.angle = 0
        self.spinning = False

        self.create_widgets()

        # 监听窗口大小变化
        self.root.bind("<Configure>", self.resize)

    def create_widgets(self):
        """创建按钮"""
        self.load_button = tk.Button(self.button_frame, text="导入抽奖内容", command=self.load_items)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.add_button = tk.Button(self.button_frame, text="添加抽奖内容", command=self.add_item)
        self.add_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.spin_button = tk.Button(self.button_frame, text="开始抽奖", command=self.start_spin)
        self.spin_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.stop_button = tk.Button(self.button_frame, text="停止抽奖", command=self.stop_spin)
        self.stop_button.pack(side=tk.LEFT, padx=5, pady=5)

    def resize(self, event):
        """调整画布大小并重绘转盘"""
        if event.width > 100 and event.height > 150:  # 防止窗口过小时错误
            self.canvas.config(width=event.width, height=event.height - 80)  # 预留按钮区域
            self.draw_wheel()

    def load_items(self):
        """加载抽奖内容"""
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                self.items = [line.strip() for line in file.readlines()]
            self.draw_wheel()

    def add_item(self):
        """添加抽奖内容"""
        item = simpledialog.askstring("添加抽奖内容", "请输入抽奖内容:")
        if item:
            self.items.append(item)
            self.draw_wheel()

    def draw_wheel(self):
        """绘制转盘"""
        self.canvas.delete("all")  # 清除画布内容

        num_items = len(self.items)
        if num_items == 0:
            self.canvas.create_text(self.canvas.winfo_width() // 2, self.canvas.winfo_height() // 2,
                                    text="请添加抽奖内容", font=("Arial", 16), fill="black")
            return

        # 获取画布尺寸
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # 计算圆盘的中心和半径
        center_x = width // 2
        center_y = height // 2
        radius = min(width, height) // 2 - 20  # 保持在画布内

        angle_step = 360 / num_items
        for i, item in enumerate(self.items):
            start_angle = (i * angle_step + self.angle) % 360  # 旋转调整
            self.canvas.create_arc(center_x - radius, center_y - radius,
                                   center_x + radius, center_y + radius,
                                   start=start_angle, extent=angle_step,
                                   fill=self.get_color(i), outline="black")

            # 计算文字位置
            mid_angle = math.radians(start_angle + angle_step / 2)
            text_x = center_x + (radius - 30) * math.cos(mid_angle)
            text_y = center_y - (radius - 30) * math.sin(mid_angle)
            self.canvas.create_text(text_x, text_y, text=item, font=("Arial", 10), fill="black")

        # 画指针
        self.canvas.create_line(center_x, center_y, center_x, center_y - radius, fill="black", width=2)

    def get_color(self, index):
        """返回颜色"""
        colors = ["red", "green", "blue", "yellow", "purple", "orange"]
        return colors[index % len(colors)]

    def start_spin(self):
        """开始旋转"""
        if not self.spinning:
            if not self.items:
                messagebox.showwarning("警告", "抽奖内容为空，请先添加或导入内容!")
                return
            self.spinning = True
            self.spin()

    def spin(self):
        """旋转动画"""
        if self.spinning:
            self.angle = (self.angle + 85) % 360  # 旋转角度更新（这里调整速度）
            self.draw_wheel()  # 重新绘制
            self.root.after(50, self.spin)  # 递归调用，实现动画

    def stop_spin(self):
        """停止旋转并显示中奖结果"""
        if self.spinning:
            self.spinning = False
            selected_index = int((self.angle / 360) * len(self.items)) % len(self.items)
            messagebox.showinfo("抽奖结果", f"恭喜你抽中了: {self.items[selected_index]}")


def cj_main():
    root = tk.Tk()
    root.iconbitmap('..\\qiqi.ico')
    app = LotteryWheel(root)
    root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = LotteryWheel(root)
    root.mainloop()
