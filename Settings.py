import pygame
import pygame_gui
import sqlite3


class Settings:
    def __init__(self, options_to_choose, name_game):
        self.name_game = name_game
        self.options_to_choose = options_to_choose
        self.database = sqlite3.connect('data/database.sql')
        self.cursor = self.database.cursor()
        self.current_choice = self.cursor.execute('''SELECT complexity from complexity_of_game
                                                      WHERE name_game=?''', (self.name_game,)).fetchone()[0]
        pygame.init()
        pygame.display.set_caption('Выберите сложность')
        self.size = self.width, self.height = 300, 130
        self.screen = pygame.display.set_mode(self.size)
        self.background = pygame.Surface((self.width, self.height))
        self.background.fill('black')
        self.setup_interface()

    def setup_interface(self):
        self.manager = pygame_gui.UIManager((self.width, self.height))
        self.choice_difficulty = pygame_gui.elements.UIDropDownMenu(options_list=self.options_to_choose,
                                                                    starting_option=self.current_choice,
                                                                    relative_rect=pygame.Rect((35, 10), (230, 50)),
                                                                    manager=self.manager)

        self.ok_button = pygame_gui.elements.UIButton(text='Ок', relative_rect=pygame.Rect((165, 70), (100, 30)),
                                                      manager=self.manager)

        self.cancel_button = pygame_gui.elements.UIButton(text='Отмена', relative_rect=pygame.Rect((35, 70), (100, 30)),
                                                          manager=self.manager)

    def get_choice(self):
        return self.choice_difficulty.selected_option

    def save_choise(self):
        self.cursor.execute("""UPDATE complexity_of_game SET complexity=?
                                WHERE name_game=?""", (self.choice_difficulty.selected_option, self.name_game))
        self.database.commit()
        self.database.close()


def start_settings(options_to_choose, name_game):
    window = Settings(options_to_choose, name_game)
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
                    if event.ui_element == window.ok_button:
                        window.save_choise()
                        running = False
                    elif event.ui_element == window.cancel_button:
                        running = False
            window.manager.process_events(event)
        window.manager.update(time_delta)
        window.screen.blit(window.background, (0, 0))
        window.manager.draw_ui(window.screen)
        pygame.display.update()