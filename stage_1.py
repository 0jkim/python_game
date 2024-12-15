# stage_1 code
# stage_1.py
from tkinter import Frame, Button, Label


class Stage1:
    def __init__(self, ui):
        self.ui = ui

    def start(self):
        # 스테이지 1 페이지 구성
        frame = Frame(self.ui.canvas, bg="black")
        Label(
            frame, text="스테이지 1", font=("Arial", 24), fg="white", bg="black"
        ).pack(pady=20)

        Button(
            frame, text="뒤로가기", font=("Arial", 16), command=self.ui.show_frame
        ).pack(pady=10)

        self.ui.show_frame(frame)
