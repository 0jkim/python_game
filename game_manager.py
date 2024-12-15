# game_manager code
# game_manager.py
from tkinter import Frame, Button, Label
from stage_1 import Stage1


class GameManager:
    def __init__(self, ui):
        self.ui = ui

    def show_main_menu(self):
        # 메인 메뉴 페이지 구성
        frame = Frame(self.ui.canvas, bg="black")
        Label(
            frame, text="웜홀 여행 게임", font=("Arial", 24), fg="white", bg="black"
        ).pack(pady=20)

        Button(
            frame,
            text="게임 시작",
            font=("Arial", 16),
            command=self.show_stage_selection,
        ).pack(pady=10)
        Button(frame, text="종료", font=("Arial", 16), command=self.ui.root.quit).pack(
            pady=10
        )

        self.ui.show_frame(frame)

    def show_stage_selection(self):
        # 스테이지 선택 페이지 구성
        frame = Frame(self.ui.canvas, bg="black")
        Label(
            frame, text="스테이지 선택", font=("Arial", 24), fg="white", bg="black"
        ).pack(pady=20)

        Button(
            frame, text="스테이지 1", font=("Arial", 16), command=self.start_stage_1
        ).pack(pady=10)
        Button(frame, text="추후 공개", font=("Arial", 16), state="disabled").pack(
            pady=10
        )
        Button(
            frame, text="뒤로가기", font=("Arial", 16), command=self.show_main_menu
        ).pack(pady=10)

        self.ui.show_frame(frame)

    def start_stage_1(self):
        # 스테이지 1 시작
        stage1 = Stage1(self.ui)
        stage1.start()
