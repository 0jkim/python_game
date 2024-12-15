from ui import GameUI
from menu_manager import MenuManager


def main():
    # UI 초기화
    ui = GameUI()
    ui.set_fullscreen(fullscreen=False)  # 전체 화면 끄기
    ui.center_window(640, 480)  # 창 크기 640x480 설정

    # 메뉴 관리
    menu_manager = MenuManager(ui)
    menu_manager.show_main_menu()

    # tkinter 메인 루프 실행
    ui.start()


if __name__ == "__main__":
    main()
