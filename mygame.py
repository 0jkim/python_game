from tkinter import *
from PIL import Image, ImageTk
import pygame
import random


class SpaceGame:
    def __init__(self):
        self.window = Tk()
        self.window.title("Space Adventure")
        self.window.geometry("1200x1000")
        self.center_window(1200, 1000)
        self.window.configure(bg="black")
        self.window.resizable(0, 0)

        # pygame for background music
        pygame.init()
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        pygame.mixer.music.load("space.mp3")
        pygame.mixer.music.play(-1)  # Loop the background music

        # Main menu setup
        self.menu_canvas = Canvas(self.window, bg="black", highlightthickness=0)
        self.menu_canvas.pack(fill="both", expand=True)

        self.menu_canvas.create_text(
            600, 200, text="Space Adventure", font=("Arial", 48, "bold"), fill="white"
        )

        self.buttons = ["게임 시작", "종료"]
        self.current_selection = 0
        self.button_labels = []
        self.render_buttons()

        self.window.bind("<Up>", self.move_selection_up)
        self.window.bind("<Down>", self.move_selection_down)
        self.window.bind("<Return>", self.select_option)

        self.window.mainloop()

    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def render_buttons(self):
        y_position = 400
        for i, label in enumerate(self.buttons):
            arrow = "👉" if i == self.current_selection else "  "
            btn_text = f"{arrow} {label}"
            button = self.menu_canvas.create_text(
                600, y_position, text=btn_text, font=("Arial", 32, "bold"), fill="white"
            )
            self.button_labels.append(button)
            y_position += 100

    def move_selection_up(self, event):
        self.current_selection = (self.current_selection - 1) % len(self.buttons)
        self.update_menu()

    def move_selection_down(self, event):
        self.current_selection = (self.current_selection + 1) % len(self.buttons)
        self.update_menu()

    def update_menu(self):
        for i, button in enumerate(self.button_labels):
            arrow = "👉" if i == self.current_selection else "  "
            text = f"{arrow} {self.buttons[i]}"
            self.menu_canvas.itemconfig(button, text=text)

    def select_option(self, event):
        if self.current_selection == 0:
            self.start_game()
        elif self.current_selection == 1:
            self.window.quit()

    def start_game(self):
        self.window.destroy()  # 메인 창 닫기
        GameScreen()


class GameScreen:
    def __init__(self):
        self.window = Tk()
        self.window.title("Space Adventure - Game")
        self.window.geometry("500x1000")
        self.center_window(500, 1000)
        self.window.configure(bg="black")
        self.window.resizable(0, 0)

        # 게임 상태 플래그
        self.running = True  # 게임 진행 상태

        # Canvas setup
        self.canvas_height = 1200  # 캔버스 높이 확장
        self.canvas = Canvas(
            self.window, bg="black", highlightthickness=0, height=self.canvas_height
        )
        self.canvas.pack(fill="both", expand=True)

        # Background setup
        self.bg_img = Image.open("space.png").resize((500, 1000))
        self.bg_photo = ImageTk.PhotoImage(self.bg_img)
        self.bg1 = self.canvas.create_image(0, 0, anchor="nw", image=self.bg_photo)
        self.bg2 = self.canvas.create_image(0, -1000, anchor="nw", image=self.bg_photo)

        # Player setup
        self.player_col = 2
        self.max_cols = 5
        self.cell_width = 500 // self.max_cols
        self.player = self.canvas.create_rectangle(
            self.cell_width * self.player_col,
            950,
            self.cell_width * (self.player_col + 1),
            1000,
            fill="blue",
        )
        self.health = 3
        self.health_text = self.canvas.create_text(
            50, 20, text=f"Health: {self.health}", font=("Arial", 16), fill="white"
        )

        # Timer setup
        self.remaining_time = 60
        self.timer_text = self.canvas.create_text(
            450,
            20,
            text=f"Time: {self.remaining_time}s",
            font=("Arial", 16),
            fill="white",
        )

        # Meteor setup
        self.meteors = []
        self.cycle_time = 1500  # 3초마다 생성
        self.meteor_speed = (1500 + 30) / (self.cycle_time / 33)  # 속도 계산
        self.spawn_meteors()

        # Key bindings
        self.window.bind("<Left>", self.move_left)
        self.window.bind("<Right>", self.move_right)

        # 게임 루프 시작
        self.update_timer()
        self.game_loop()

    def center_window(self, width, height):
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.window.geometry(f"{width}x{height}+{x}+{y}")

    def move_background(self):
        self.canvas.move(self.bg1, 0, 5)
        self.canvas.move(self.bg2, 0, 5)
        if self.canvas.coords(self.bg1)[1] >= 1000:
            self.canvas.moveto(self.bg1, 0, -1000)
        if self.canvas.coords(self.bg2)[1] >= 1000:
            self.canvas.moveto(self.bg2, 0, -1000)

    def move_left(self, event):
        if self.player_col > 0:
            self.player_col -= 1
            self.update_player_position()

    def move_right(self, event):
        if self.player_col < self.max_cols - 1:
            self.player_col += 1
            self.update_player_position()

    def update_player_position(self):
        self.canvas.coords(
            self.player,
            self.cell_width * self.player_col,
            950,
            self.cell_width * (self.player_col + 1),
            1000,
        )

    def spawn_meteors(self):
        self.meteors = []
        num_meteors = random.randint(2, 4)
        for _ in range(num_meteors):
            col = random.randint(0, self.max_cols - 1)
            meteor = self.canvas.create_rectangle(
                self.cell_width * col, -30, self.cell_width * (col + 1), 0, fill="red"
            )
            self.meteors.append(meteor)
        self.window.after(self.cycle_time, self.spawn_meteors)

    def move_meteors(self):
        for meteor in self.meteors[:]:
            # 운석 이동
            self.canvas.move(meteor, 0, self.meteor_speed)
            coords = self.canvas.coords(meteor)

            # 운석이 캔버스 높이를 넘어간 경우 삭제
            if coords[1] >= self.canvas_height:
                print(f"Removing meteor off-screen at coords: {coords}")
                self.meteors.remove(meteor)  # 리스트에서 제거
                self.canvas.delete(meteor)  # 캔버스에서 제거
                continue  # 다른 조건과 충돌 방지

            # 운석과 우주선 충돌 감지
            if self.check_collision(meteor):
                print(f"Collision detected with meteor at coords: {coords}")
                self.health -= 1
                self.canvas.itemconfig(self.health_text, text=f"Health: {self.health}")
                self.meteors.remove(meteor)
                self.canvas.delete(meteor)
                if self.health <= 0:
                    self.end_game()
                    return

    def check_collision(self, meteor):
        player_coords = self.canvas.coords(self.player)
        meteor_coords = self.canvas.coords(meteor)
        return (
            player_coords[2] > meteor_coords[0]
            and player_coords[0] < meteor_coords[2]
            and player_coords[3] > meteor_coords[1]
            and player_coords[1] < meteor_coords[3]
        )

    def update_timer(self):
        self.remaining_time -= 1
        self.canvas.itemconfig(self.timer_text, text=f"Time: {self.remaining_time}s")
        if self.remaining_time <= 0:  # 남은 시간이 0초일 때 성공 처리
            self.end_game(success=True)
        else:
            self.window.after(1000, self.update_timer)

    def end_game(self, success=False):
        self.running = False
        if success:
            message = "Mission Complete!"
        else:
            message = "Mission Over!"

        self.canvas.create_text(
            250,
            500,
            text=message,
            font=("Arial", 48, "bold"),
            fill="green" if success else "red",
        )
        self.window.after(3000, self.return_to_main_menu)

    def return_to_main_menu(self):
        self.window.destroy()
        SpaceGame()  # 메인 페이지로 돌아가기

    def game_loop(self):
        if self.running:
            self.move_background()
            self.move_meteors()
            self.window.after(33, self.game_loop)


if __name__ == "__main__":
    # 프로그램 실행 진입점
    SpaceGame()
