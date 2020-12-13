import pygame
import pygame_gui
from AssetManager import assetManager


class MiniGames_launcher():
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('MiniGames_launcher')
        self.size = self.width, self.height = 400, 600
        self.screen = pygame.display.set_mode(self.size)
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill('black')
        self.setup_interface()

    def setup_interface(self):
        font = pygame.font.SysFont('Gothic', 90)
        text = font.render("MiniGames", True, (100, 255, 100))
        text_x = self.width // 2 - text.get_width() // 2
        text_y = 100
        self.background.blit(text, (text_x, text_y))
        self.manager = pygame_gui.UIManager((self.width, self.height))

        self.start_tetris_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((63, 200), (200, 70)),
                                                                text='Тетрис',
                                                                manager=self.manager)

        self.start_settings_tetris_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((267, 200), (70, 70)),
            text='...',
            manager=self.manager)

        self.start_minesweeper_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((63, 300), (200, 70)),
                                                                     text='Сапёр',
                                                                     manager=self.manager)

        self.start_settings_minesweeper_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((267, 300), (70, 70)),
            text='...',
            manager=self.manager)

    def start_minesweeper(self):
        print('start_minesweeper')

    def start_tetris(self):
        print('start_tetris')

    def start_settings_minesweeper(self):
        print('start_settings_minesweeper')

    def start_settings_tetris(self):
        print('start_settings_tetris')


if __name__ == '__main__':
    window = MiniGames_launcher()
    fps = 50
    clock = pygame.time.Clock()
    running = True
    while running:
        time_delta = clock.tick(fps) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    if event.ui_element == window.start_tetris_button:
                        window.start_tetris()
                    elif event.ui_element == window.start_settings_tetris_button:
                        window.start_settings_tetris()
                    elif event.ui_element == window.start_minesweeper_button:
                        window.start_minesweeper()
                    elif event.ui_element == window.start_settings_minesweeper_button:
                        window.start_settings_minesweeper()
            window.manager.process_events(event)
        window.manager.update(time_delta)
        window.screen.blit(window.background, (0, 0))
        window.manager.draw_ui(window.screen)
        pygame.display.update()
