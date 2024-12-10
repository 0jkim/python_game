import tkinter as tk
import random
import time

# Constants
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
CELL_WIDTH = WINDOW_WIDTH // 3
PLAYER_SIZE = 50
ENEMY_SIZE = 50
BULLET_SIZE = 10
UPGRADE_SIZE = 20
FPS = 60
STAGE_DURATION = 60  # 스테이지 1 클리어 시간 (초)
INITIAL_BULLET_INTERVAL = 1000  # 기본 총알 발사 주기 (1초)
INITIAL_ENEMY_SPAWN_INTERVAL = 500  # 기본 적 스폰 주기 (0.5초)
UPGRADE_SPAWN_INTERVAL = 5000  # 업그레이드 블록 스폰 주기 (5초)
ENEMY_SPEED = 1  # 적 이동 속도
BULLET_SPEED = 10  # 총알 이동 속도


class Player:
    def __init__(self, canvas):
        self.canvas = canvas
        self.row = 1  # 초기 위치 (중앙 칸)
        self.y = WINDOW_HEIGHT - PLAYER_SIZE
        self.player = canvas.create_rectangle(
            CELL_WIDTH * self.row + CELL_WIDTH // 2 - PLAYER_SIZE // 2,
            self.y - PLAYER_SIZE,
            CELL_WIDTH * self.row + CELL_WIDTH // 2 + PLAYER_SIZE // 2,
            self.y,
            fill="blue",
        )
        self.weapon_level = 1  # 총알 레벨
        self.bullet_speed = BULLET_SPEED  # 총알 속도
        self.bullet_interval = INITIAL_BULLET_INTERVAL  # 총알 발사 주기

    def move(self, direction):
        if direction == "left" and self.row > 0:
            self.row -= 1
        elif direction == "right" and self.row < 2:
            self.row += 1
        self.update_position()

    def update_position(self):
        x = CELL_WIDTH * self.row + CELL_WIDTH // 2
        self.canvas.coords(
            self.player,
            x - PLAYER_SIZE // 2,
            self.y - PLAYER_SIZE,
            x + PLAYER_SIZE // 2,
            self.y,
        )

    def shoot(self):
        return Bullet(self.canvas, self.row, self.bullet_speed)


class Bullet:
    def __init__(self, canvas, row, speed):
        self.canvas = canvas
        self.row = row
        self.y = WINDOW_HEIGHT - PLAYER_SIZE - BULLET_SIZE
        self.speed = speed
        self.bullet = canvas.create_oval(
            CELL_WIDTH * self.row + CELL_WIDTH // 2 - BULLET_SIZE // 2,
            self.y - BULLET_SIZE,
            CELL_WIDTH * self.row + CELL_WIDTH // 2 + BULLET_SIZE // 2,
            self.y,
            fill="yellow",
        )

    def move(self):
        self.y -= self.speed  # 총알 이동 속도
        self.canvas.move(self.bullet, 0, -self.speed)

    def is_off_screen(self):
        return self.y < 0


class Enemy:
    def __init__(self, canvas):
        self.canvas = canvas
        self.row = random.randint(0, 2)  # 적은 3칸 중 하나에서 스폰
        self.y = -ENEMY_SIZE
        self.enemy = canvas.create_rectangle(
            CELL_WIDTH * self.row + CELL_WIDTH // 2 - ENEMY_SIZE // 2,
            self.y,
            CELL_WIDTH * self.row + CELL_WIDTH // 2 + ENEMY_SIZE // 2,
            self.y + ENEMY_SIZE,
            fill="red",
        )

    def move(self):
        self.y += ENEMY_SPEED  # 적의 이동 속도
        self.canvas.coords(
            self.enemy,
            CELL_WIDTH * self.row + CELL_WIDTH // 2 - ENEMY_SIZE // 2,
            self.y,
            CELL_WIDTH * self.row + CELL_WIDTH // 2 + ENEMY_SIZE // 2,
            self.y + ENEMY_SIZE,
        )

    def is_off_screen(self):
        return self.y > WINDOW_HEIGHT


class Upgrade:
    def __init__(self, canvas):
        self.canvas = canvas
        self.row = random.randint(0, 2)  # 업그레이드 블록은 3칸 중 하나에서 스폰
        self.y = -UPGRADE_SIZE
        self.block = canvas.create_oval(
            CELL_WIDTH * self.row + CELL_WIDTH // 2 - UPGRADE_SIZE // 2,
            self.y,
            CELL_WIDTH * self.row + CELL_WIDTH // 2 + UPGRADE_SIZE // 2,
            self.y + UPGRADE_SIZE,
            fill="green",
        )

    def move(self):
        self.y += ENEMY_SPEED  # 업그레이드 블록의 이동 속도
        self.canvas.coords(
            self.block,
            CELL_WIDTH * self.row + CELL_WIDTH // 2 - UPGRADE_SIZE // 2,
            self.y,
            CELL_WIDTH * self.row + CELL_WIDTH // 2 + UPGRADE_SIZE // 2,
            self.y + UPGRADE_SIZE,
        )

    def is_off_screen(self):
        return self.y > WINDOW_HEIGHT


class Stage1:
    def __init__(self, canvas, on_cleared_callback):
        self.canvas = canvas
        self.on_cleared_callback = on_cleared_callback
        self.start_time = None
        self.running = False
        self.player = Player(canvas)
        self.enemies = []
        self.bullets = []
        self.upgrades = []
        self.enemy_spawn_interval = INITIAL_ENEMY_SPAWN_INTERVAL
        self.lives = 3

        self.canvas.bind_all("<Left>", lambda e: self.player.move("left"))
        self.canvas.bind_all("<Right>", lambda e: self.player.move("right"))
        self.start()

    def start(self):
        self.running = True
        self.start_time = time.time()
        self.spawn_enemy()
        self.spawn_upgrade()
        self.shoot_bullet()
        self.game_loop()

    def game_loop(self):
        if not self.running:
            return

        elapsed_time = time.time() - self.start_time
        if elapsed_time >= STAGE_DURATION:
            self.running = False
            self.on_cleared_callback()
            return

        self.canvas.delete("timer")
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            50,
            text=f"남은 시간: {STAGE_DURATION - int(elapsed_time)}초",
            fill="white",
            font=("Arial", 16),
            tag="timer",
        )

        # Move bullets
        for bullet in self.bullets[:]:
            bullet.move()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
                self.canvas.delete(bullet.bullet)

        # Move enemies
        for enemy in self.enemies[:]:
            enemy.move()
            if enemy.is_off_screen():
                self.enemies.remove(enemy)
                self.canvas.delete(enemy.enemy)
                self.lives -= 1
            else:
                for bullet in self.bullets[:]:
                    if self._check_collision(bullet.bullet, enemy.enemy):
                        self.enemies.remove(enemy)
                        self.bullets.remove(bullet)
                        self.canvas.delete(enemy.enemy)
                        self.canvas.delete(bullet.bullet)
                        break

        # Move upgrades
        for upgrade in self.upgrades[:]:
            upgrade.move()
            if upgrade.is_off_screen():
                self.upgrades.remove(upgrade)
                self.canvas.delete(upgrade.block)
            elif self._check_collision(self.player.player, upgrade.block):
                self.upgrades.remove(upgrade)
                self.canvas.delete(upgrade.block)
                self.player.bullet_interval = max(100, self.player.bullet_interval // 3)
                self.enemy_spawn_interval = max(100, self.enemy_spawn_interval // 3)

        self.canvas.after(1000 // FPS, self.game_loop)

    def spawn_enemy(self):
        if self.running:
            self.enemies.append(Enemy(self.canvas))
            self.canvas.after(self.enemy_spawn_interval, self.spawn_enemy)

    def spawn_upgrade(self):
        if self.running:
            self.upgrades.append(Upgrade(self.canvas))
            self.canvas.after(UPGRADE_SPAWN_INTERVAL, self.spawn_upgrade)

    def shoot_bullet(self):
        if self.running:
            self.bullets.append(self.player.shoot())
            self.canvas.after(self.player.bullet_interval, self.shoot_bullet)

    def _check_collision(self, obj1, obj2):
        coords1 = self.canvas.coords(obj1)
        coords2 = self.canvas.coords(obj2)
        return not (
            coords1[2] < coords2[0]
            or coords1[0] > coords2[2]
            or coords1[3] < coords2[1]
            or coords1[1] > coords2[3]
        )


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
            text="스테이지 2: 어려운 모드 (준비 중)",
            fill="white",
            font=("Arial", 16),
            tag="stage2",
        )
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            300,
            text="스테이지 3: 매우 어려운 모드 (준비 중)",
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
        elif self.stage_selection_index == 4:
            self.show_main_menu()

    def start_stage_1(self):
        """스테이지 1 실행"""
        self.canvas.delete("all")
        self.stage = Stage1(self.canvas, self.stage_cleared)
        self.stage.start()

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
