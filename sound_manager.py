import pygame


class GameSound:
    def __init__(self, bgm_path="space.mp3"):
        pygame.init()
        pygame.mixer.init()

        # 배경음악 설정 및 재생
        try:
            pygame.mixer.music.load(bgm_path)
            pygame.mixer.music.play(-1)  # 반복 재생
        except pygame.error as e:
            print(f"Error loading background music: {e}")

    def stop_bgm(self):
        """배경음악 정지"""
        pygame.mixer.music.stop()

    def pause_bgm(self):
        """배경음악 일시 정지"""
        pygame.mixer.music.pause()

    def resume_bgm(self):
        """배경음악 재개"""
        pygame.mixer.music.unpause()
