from tkinter import PhotoImage
from PIL import Image, ImageTk


class Background:
    def __init__(self, canvas, window_width, window_height, image_path):
        self.canvas = canvas
        self.window_width = window_width
        self.window_height = window_height
        self.move_speed = 2  # 배경 이동 속도 (Y축 방향)

        # 배경 이미지 초기화
        self.bgimg = PhotoImage(file=image_path)
        self.bg1 = self.canvas.create_image(
            0, 0, image=self.bgimg, tags="bg", anchor="nw"
        )
        self.bg2 = self.canvas.create_image(
            0, -window_height, image=self.bgimg, tags="bg", anchor="nw"
        )

    def move(self):
        """배경 위아래 이동"""
        self.canvas.move(self.bg1, 0, self.move_speed)
        self.canvas.move(self.bg2, 0, self.move_speed)

        # bg1이 화면 아래로 벗어나면 위로 이동
        if self.canvas.coords(self.bg1)[1] >= self.window_height:
            self.canvas.moveto(self.bg1, 0, -self.window_height)

        # bg2가 화면 아래로 벗어나면 위로 이동
        if self.canvas.coords(self.bg2)[1] >= self.window_height:
            self.canvas.moveto(self.bg2, 0, -self.window_height)
