from tkinter import Button
from sound_manager import GameSound


class MenuManager:
    def __init__(self, ui):
        self.ui = ui
        self.canvas = ui.canvas
        self.sound_manager = GameSound()  # 배경음악 초기화

    def show_main_menu(self):
        # 캔버스에 텍스트 추가
        self.canvas.create_text(
            320, 150, font="Times 30 bold", text="Basic Form", fill="red"
        )
        self.canvas.create_text(
            320,
            200,
            font="Times 13 italic bold",
            text="Department of Computer Science and Engineering,\nGyeongsang National University",
            fill="white",
        )

        # 버튼 추가
        self.add_buttons()

    def add_buttons(self):
        # 게임 시작 버튼
        start_button = Button(
            self.ui.root,
            text="게임 시작",
            font="Arial 16 bold",
            bg="gray",
            fg="white",
            command=self.start_game,
        )
        start_button.place(relx=0.5, rely=0.5, anchor="center", y=-30)

        # 종료 버튼
        exit_button = Button(
            self.ui.root,
            text="종료",
            font="Arial 16 bold",
            bg="gray",
            fg="white",
            command=self.exit_game,
        )
        exit_button.place(relx=0.5, rely=0.5, anchor="center", y=30)

    def start_game(self):
        print("게임 시작 버튼 클릭됨")  # 스테이지 전환 로직 추가 가능

    def exit_game(self):
        self.sound_manager.stop_bgm()  # 배경음악 정지
        self.ui.root.quit()  # 프로그램 종료
