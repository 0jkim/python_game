import random
import time
from tkinter import Canvas

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
    def __init__(self, canvas: Canvas):
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
        return Bullet(self.canvas, self.row, self.bullet_speed, self.weapon_level)


class Bullet:
    def __init__(self, canvas: Canvas, row, speed, level):
        self.canvas = canvas
        self.row = row
        self.y = WINDOW_HEIGHT - PLAYER_SIZE - BULLET_SIZE
        self.speed = speed
        self.level = min(level, 3)  # 최대 3개의 열
        self.bullets = []

        # 총알 모양 결정
        bullet_shape = self._get_bullet_shape()

        # 최대 3개의 열 생성
        for offset in range(-(self.level - 1), self.level):  # 업그레이드된 총알 수
            x = CELL_WIDTH * self.row + CELL_WIDTH // 2 + offset * 10
            self.bullets.append(
                canvas.create_oval(
                    x - bullet_shape[0],
                    self.y - bullet_shape[1],
                    x + bullet_shape[0],
                    self.y + bullet_shape[1],
                    fill="yellow",
                )
            )

    def _get_bullet_shape(self):
        """총알 모양 반환 (업그레이드 여부에 따라)"""
        if self.level > 1:
            return (5, 15)  # 업그레이드된 총알은 긴 타원형
        return (5, 5)  # 기본 총알은 원형

    def move(self):
        self.y -= self.speed  # 총알 이동 속도
        for bullet in self.bullets:
            self.canvas.move(bullet, 0, -self.speed)

    def is_off_screen(self):
        return self.y < 0


class Enemy:
    def __init__(self, canvas: Canvas, health=1):
        self.canvas = canvas
        self.row = random.randint(0, 2)  # 적은 3칸 중 하나에서 스폰
        self.y = -ENEMY_SIZE
        self.health = health  # 몹 체력
        self.color = "purple" if health > 1 else "red"  # 체력 10인 몹은 보라색
        self.enemy = canvas.create_rectangle(
            CELL_WIDTH * self.row + CELL_WIDTH // 2 - ENEMY_SIZE // 2,
            self.y,
            CELL_WIDTH * self.row + CELL_WIDTH // 2 + ENEMY_SIZE // 2,
            self.y + ENEMY_SIZE,
            fill=self.color,
        )
        self.health_text = canvas.create_text(
            CELL_WIDTH * self.row + CELL_WIDTH // 2,
            self.y + ENEMY_SIZE // 2,
            text=str(self.health),
            fill="white",
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
        self.canvas.coords(
            self.health_text,
            CELL_WIDTH * self.row + CELL_WIDTH // 2,
            self.y + ENEMY_SIZE // 2,
        )

    def take_damage(self):
        """몹이 데미지를 받을 때 체력 감소"""
        self.health -= 1
        if self.health > 0:
            self.canvas.itemconfig(self.health_text, text=str(self.health))  # 체력 갱신
        else:
            self.delete()

    def delete(self):
        """몹 삭제"""
        self.canvas.delete(self.enemy)
        self.canvas.delete(self.health_text)

    def is_off_screen(self):
        return self.y > WINDOW_HEIGHT


class Upgrade:
    def __init__(self, canvas: Canvas, upgrade_type="rate"):
        self.canvas = canvas
        self.row = random.randint(0, 2)  # 업그레이드 블록은 3칸 중 하나에서 스폰
        self.y = -UPGRADE_SIZE
        self.upgrade_type = upgrade_type
        self.color = "green" if upgrade_type == "rate" else "blue"
        self.block = canvas.create_oval(
            CELL_WIDTH * self.row + CELL_WIDTH // 2 - UPGRADE_SIZE // 2,
            self.y,
            CELL_WIDTH * self.row + CELL_WIDTH // 2 + UPGRADE_SIZE // 2,
            self.y + UPGRADE_SIZE,
            fill=self.color,
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
    def __init__(self, canvas: Canvas, on_cleared_callback):
        self.canvas = canvas
        self.on_cleared_callback = on_cleared_callback
        self.start_time = None
        self.running = False
        self.player = Player(canvas)
        self.enemies = []
        self.bullets = []
        self.upgrades = []
        self.enemy_spawn_interval = INITIAL_ENEMY_SPAWN_INTERVAL
        self.enemy_spawn_interval_high_health = 5000  # 체력 10 몹 초기 생성 주기
        self.lives = 10  # 사용자 체력
        self.upgrade_count_bullet_rate = 0  # 총알 발사 주기 업그레이드 횟수
        self.upgrade_count_bullet_level = 0  # 총알 개수 업그레이드 횟수
        self.max_bullet_level = 3  # 총알 최대 열 제한
        self.max_bullet_rate_upgrades = 10  # 총알 발사 주기 최대 업그레이드 횟수

        # 체력 표시
        self.health_text = self.canvas.create_text(
            WINDOW_WIDTH // 2,
            WINDOW_HEIGHT - 20,
            text=f"체력: {self.lives}",
            fill="white",
            font=("Arial", 16),
        )

        # 하단 가로선
        self.health_line = self.canvas.create_line(
            0,
            WINDOW_HEIGHT - PLAYER_SIZE - 10,
            WINDOW_WIDTH,
            WINDOW_HEIGHT - PLAYER_SIZE - 10,
            fill="red",
        )

        self.canvas.bind_all("<Left>", lambda e: self.player.move("left"))
        self.canvas.bind_all("<Right>", lambda e: self.player.move("right"))
        self.start()

    def start(self):
        self.running = True
        self.start_time = time.time()
        self.spawn_enemy()  # 체력 1 몹 생성
        self.spawn_high_health_enemy()  # 체력 10 몹 생성
        self.spawn_upgrade()
        self.shoot_bullet()
        self.game_loop()

    def spawn_enemy(self):
        """체력 1 몹 생성"""
        if self.running:
            enemy = Enemy(self.canvas, health=1)
            self.enemies.append(enemy)
            self.canvas.after(self.enemy_spawn_interval, self.spawn_enemy)

    def spawn_high_health_enemy(self):
        """체력 10 몹 생성"""
        if self.running:
            elapsed_time = time.time() - self.start_time
            if elapsed_time >= 20:  # 체력 10 몹은 20초 이후부터 생성
                enemy = Enemy(self.canvas, health=10)
                self.enemies.append(enemy)
                self.enemy_spawn_interval_high_health = max(
                    1000, self.enemy_spawn_interval_high_health // 6
                )
            self.canvas.after(
                self.enemy_spawn_interval_high_health, self.spawn_high_health_enemy
            )

    def spawn_upgrade(self):
        """업그레이드 블록 생성"""
        if self.running:
            # 제한 조건에 따라 업그레이드 블록 생성
            if (
                self.upgrade_count_bullet_rate < self.max_bullet_rate_upgrades
                or self.upgrade_count_bullet_level < self.max_bullet_level
            ):
                upgrade_type = "rate" if random.random() < 0.5 else "level"

                # 제한 조건 확인
                if (
                    upgrade_type == "rate"
                    and self.upgrade_count_bullet_rate >= self.max_bullet_rate_upgrades
                ):
                    upgrade_type = "level"
                if (
                    upgrade_type == "level"
                    and self.upgrade_count_bullet_level >= self.max_bullet_level
                ):
                    upgrade_type = "rate"

                self.upgrades.append(Upgrade(self.canvas, upgrade_type))
                print(f"Spawned Upgrade: {upgrade_type}")  # 디버깅용 출력
            self.canvas.after(UPGRADE_SPAWN_INTERVAL, self.spawn_upgrade)

    def shoot_bullet(self):
        """총알 발사"""
        if self.running:
            bullet = self.player.shoot()
            self.bullets.append(bullet)
            self.canvas.after(self.player.bullet_interval, self.shoot_bullet)

    def game_loop(self):
        """게임 루프"""
        if not self.running:
            return

        elapsed_time = time.time() - self.start_time
        self.canvas.delete("timer")
        self.canvas.create_text(
            WINDOW_WIDTH // 2,
            50,
            text=f"남은 시간: {STAGE_DURATION - int(elapsed_time)}초",
            fill="white",
            font=("Arial", 16),
            tag="timer",
        )

        bullets_to_remove = []
        enemies_to_remove = []

        # 총알 이동 및 충돌 처리
        for bullet in self.bullets:
            bullet.move()
            if bullet.is_off_screen():
                bullets_to_remove.append(bullet)
                for b in bullet.bullets:
                    self.canvas.delete(b)

            for enemy in self.enemies:
                for b in bullet.bullets[:]:
                    if self._check_collision(b, enemy.enemy):
                        try:
                            bullet.bullets.remove(b)
                            self.canvas.delete(b)
                        except ValueError:
                            continue

                        if enemy.health > 1:
                            enemy.take_damage()  # 몹 체력 감소
                        else:
                            enemies_to_remove.append(enemy)
                        break

        # 적 이동 및 체력 선 충돌 확인
        for enemy in self.enemies:
            enemy.move()
            if enemy.is_off_screen():
                enemies_to_remove.append(enemy)
            elif enemy.y >= WINDOW_HEIGHT - PLAYER_SIZE - 10:  # 체력 선을 넘음
                enemies_to_remove.append(enemy)
                self.lives -= 1
                self.canvas.itemconfig(self.health_text, text=f"체력: {self.lives}")

                if self.lives <= 0:
                    self.running = False
                    self.canvas.create_text(
                        WINDOW_WIDTH // 2,
                        WINDOW_HEIGHT // 2,
                        text="Game Over",
                        fill="red",
                        font=("Arial", 32),
                    )
                    return

        # 업그레이드 이동 및 충돌 확인
        for upgrade in self.upgrades[:]:
            upgrade.move()
            if upgrade.is_off_screen():
                self.upgrades.remove(upgrade)
                self.canvas.delete(upgrade.block)
            elif self._check_collision(self.player.player, upgrade.block):
                self.upgrades.remove(upgrade)
                self.canvas.delete(upgrade.block)
                self.handle_upgrade(upgrade.upgrade_type)

        # 삭제 대기 리스트에서 제거
        for bullet in bullets_to_remove:
            if bullet in self.bullets:
                self.bullets.remove(bullet)

        for enemy in enemies_to_remove:
            if enemy in self.enemies:
                enemy.delete()
                self.enemies.remove(enemy)

        self.canvas.after(1000 // FPS, self.game_loop)

    def handle_upgrade(self, upgrade_type):
        """업그레이드 효과 처리"""
        if (
            upgrade_type == "rate"
            and self.upgrade_count_bullet_rate < self.max_bullet_rate_upgrades
        ):
            self.player.bullet_interval = max(100, self.player.bullet_interval // 2)
            self.upgrade_count_bullet_rate += 1
        elif (
            upgrade_type == "level"
            and self.upgrade_count_bullet_level < self.max_bullet_level
        ):
            self.player.weapon_level = min(
                self.max_bullet_level, self.player.weapon_level + 1
            )
            self.upgrade_count_bullet_level += 1

    def _check_collision(self, obj1, obj2):
        """충돌 감지"""
        try:
            coords1 = self.canvas.coords(obj1)
            coords2 = self.canvas.coords(obj2)
            if not coords1 or not coords2:
                return False
        except IndexError:
            return False

        return not (
            coords1[2] < coords2[0]
            or coords1[0] > coords2[2]
            or coords1[3] < coords2[1]
            or coords1[1] > coords2[3]
        )
