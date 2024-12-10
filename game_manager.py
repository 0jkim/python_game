import tkinter as tk
from stage1 import Stage1

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600


class GameManager:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Shooting Game")
        self.canvas = tk.Canvas(
            self.root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="black"
        )
        self.canvas.pack()
        self.main_menu_index = 1  # 기본 선택: 게임 시작
        self.stage_selection_index = 1  # 기본 선택: 스테이지 1
        self.show_main_menu()

    def show_main_menu(self):
        """초기 설정 창"""
        self.canvas.delete("all")
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            100,
            text="Shooting Game",
            fill="white",
            font=("Arial", 24),
        )
        self.canvas.create_text(
            50, 200, text=">", fill="yellow", font=("Arial", 16), tag="pointer"
        )
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            200,
            text="게임 시작",
            fill="white",
            font=("Arial", 16),
            tag="start",
        )
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            250,
            text="종료",
            fill="white",
            font=("Arial", 16),
            tag="exit",
        )
        self.root.bind("<Up>", self.navigate_main_menu)
        self.root.bind("<Down>", self.navigate_main_menu)
        self.root.bind("<Return>", self.select_main_menu)

    def navigate_main_menu(self, event):
        """메인 메뉴 항목 이동"""
        if event.keysym == "Up" and self.main_menu_index > 1:
            self.main_menu_index -= 1
        elif event.keysym == "Down" and self.main_menu_index < 2:
            self.main_menu_index += 1

        self.update_main_menu_pointer()

    def update_main_menu_pointer(self):
        """포인터 업데이트"""
        self.canvas.delete("pointer")
        if self.main_menu_index == 1:
            self.canvas.create_text(
                50, 200, text=">", fill="yellow", font=("Arial", 16), tag="pointer"
            )
        elif self.main_menu_index == 2:
            self.canvas.create_text(
                50, 250, text=">", fill="yellow", font=("Arial", 16), tag="pointer"
            )

    def select_main_menu(self, event):
        """메인 메뉴 선택"""
        if self.main_menu_index == 1:
            self.show_stage_selection()
        elif self.main_menu_index == 2:
            self.root.quit()

    def show_stage_selection(self):
        """스테이지 선택 화면"""
        self.canvas.delete("all")
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            100,
            text="스테이지 선택",
            fill="white",
            font=("Arial", 20),
        )
        self.canvas.create_text(
            50, 200, text=">", fill="yellow", font=("Arial", 16), tag="pointer"
        )
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            200,
            text="스테이지 1: 기본 모드",
            fill="white",
            font=("Arial", 16),
            tag="stage1",
        )
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            250,
            text="스테이지 2: 어려운 모드",
            fill="white",
            font=("Arial", 16),
            tag="stage2",
        )
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            300,
            text="스테이지 3: 매우 어려운 모드",
            fill="white",
            font=("Arial", 16),
            tag="stage3",
        )
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            400,
            text="뒤로 가기",
            fill="white",
            font=("Arial", 16),
            tag="back",
        )
        self.root.bind("<Up>", self.navigate_stage_selection)
        self.root.bind("<Down>", self.navigate_stage_selection)
        self.root.bind("<Return>", self.select_stage)

    def navigate_stage_selection(self, event):
        """스테이지 선택 이동"""
        if event.keysym == "Up" and self.stage_selection_index > 1:
            self.stage_selection_index -= 1
        elif event.keysym == "Down" and self.stage_selection_index < 4:
            self.stage_selection_index += 1

        self.update_stage_pointer()

    def update_stage_pointer(self):
        """스테이지 선택 포인터 업데이트"""
        self.canvas.delete("pointer")
        y_positions = {1: 200, 2: 250, 3: 300, 4: 400}
        self.canvas.create_text(
            50,
            y_positions[self.stage_selection_index],
            text=">",
            fill="yellow",
            font=("Arial", 16),
            tag="pointer",
        )

    def select_stage(self, event):
        """스테이지 선택"""
        if self.stage_selection_index == 1:
            self.start_stage_1()
        elif self.stage_selection_index == 2:
            self.start_stage_2()
        elif self.stage_selection_index == 3:
            self.start_stage_3()
        elif self.stage_selection_index == 4:
            self.show_main_menu()

    def start_stage_1(self):
        """스테이지 1 실행"""
        self.canvas.delete("all")
        self.stage = Stage1(self.canvas, self.stage_cleared)
        self.stage.start()

    # def start_stage_2(self):
    #     """스테이지 2 실행"""
    #     self.canvas.delete("all")
    #     self.stage = Stage2(self.canvas, self.stage_cleared)
    #     self.stage.start()

    # def start_stage_3(self):
    #     """스테이지 3 실행"""
    #     self.canvas.delete("all")
    #     self.stage = Stage3(self.canvas, self.stage_cleared)
    #     self.stage.start()

    def stage_cleared(self):
        """스테이지 클리어 후 처리"""
        self.canvas.delete("all")
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            100,
            text="스테이지 클리어!",
            fill="white",
            font=("Arial", 24),
        )
        self.root.after(3000, self.show_stage_selection)


if __name__ == "__main__":
    game = GameManager()
    game.root.mainloop()
