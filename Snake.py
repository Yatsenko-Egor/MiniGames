import pygame
from Apple import Apple
from Field import Field
import sqlite3


class Snake:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Змейка')
        self.LINK_SIZE = 25
        self.speed = 25
        self.length_body = 2
        self.size = self.width, self.height = 600, 600
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill((34, 139, 34))
        self.snake_body = [[300, 200], [300, 225]]
        self.tongue_state = 0
        self.tongue_len = 7
        self.direction = 2
        self.stop_game = True
        self.field = Field()
        self.generate_apple()
        self.field.draw(self.screen)
        self.draw_snake()
        self.start()

    def draw_snake(self):
        for link in self.snake_body:
            pygame.draw.rect(self.screen, (0, 0, 255), ((link[0], link[1]), (self.LINK_SIZE, self.LINK_SIZE)))
            if self.snake_body.index(link) != self.length_body - 1:
                pygame.draw.circle(self.screen, (0, 255, 0), (link[0] + 13, link[1] + 13), 3)
            else:
                if self.direction == 2:
                    left_eye_x = link[0] + 5
                    left_eye_y = link[1] + 12
                    right_eye_x = link[0] + 20
                    right_eye_y = link[1] + 12
                    left_nostril_x = link[0] + 6
                    left_nostril_y = link[1] + 18
                    right_nostril_x = link[0] + 17
                    right_nostril_y = link[1] + 18
                    tongue_x = link[0] + 11
                    tongue_y = link[1] + 25
                    size_tongue = (3, self.tongue_len)
                elif self.direction == 0:
                    left_eye_x = link[0] + 5
                    left_eye_y = link[1] + 13
                    right_eye_x = link[0] + 20
                    right_eye_y = link[1] + 13
                    left_nostril_x = link[0] + 6
                    left_nostril_y = link[1] + 5
                    right_nostril_x = link[0] + 17
                    right_nostril_y = link[1] + 5
                    tongue_x = link[0] + 11
                    tongue_y = link[1] - self.tongue_len
                    size_tongue = (3, self.tongue_len)
                elif self.direction == 1:
                    left_eye_x = link[0] + 12
                    left_eye_y = link[1] + 5
                    right_eye_x = link[0] + 12
                    right_eye_y = link[1] + 20
                    left_nostril_x = link[0] + 18
                    left_nostril_y = link[1] + 6
                    right_nostril_x = link[0] + 18
                    right_nostril_y = link[1] + 17
                    tongue_x = link[0] + 25
                    tongue_y = link[1] + 11
                    size_tongue = (self.tongue_len, 3)
                elif self.direction == 3:
                    left_eye_x = link[0] + 13
                    left_eye_y = link[1] + 5
                    right_eye_x = link[0] + 13
                    right_eye_y = link[1] + 20
                    left_nostril_x = link[0] + 5
                    left_nostril_y = link[1] + 6
                    right_nostril_x = link[0] + 5
                    right_nostril_y = link[1] + 17
                    tongue_x = link[0] - self.tongue_len
                    tongue_y = link[1] + 11
                    size_tongue = (self.tongue_len, 3)
                pygame.draw.circle(self.screen, (255, 0, 0), (left_eye_x, left_eye_y), 2)
                pygame.draw.circle(self.screen, (255, 0, 0), (right_eye_x, right_eye_y), 2)
                pygame.draw.rect(self.screen, (0, 0, 0), ((left_nostril_x, left_nostril_y), (1, 1)))
                pygame.draw.rect(self.screen, (0, 0, 0), ((right_nostril_x, right_nostril_y), (1, 1)))
                pygame.draw.rect(self.screen, (255, 0, 0), ((tongue_x, tongue_y), size_tongue))

    def change_tongue(self):
        if self.tongue_state:
            self.tongue_len += 1
            if self.tongue_len == 7:
                self.tongue_state = 0
        else:
            self.tongue_len -= 1
            if self.tongue_len == 0:
                self.tongue_state = 1

    def move_snake(self):
        x_head, y_head = self.snake_body[-1]
        if self.direction == 0:
            y_head -= self.speed
        elif self.direction == 1:
            x_head += self.speed
        elif self.direction == 2:
            y_head += self.speed
        elif self.direction == 3:
            x_head -= self.speed
        if self.can_move(x_head, y_head):
            self.snake_body.append([x_head, y_head])
            if len(self.snake_body) > self.length_body:
                self.snake_body.pop(0)
        else:
            self.loss()

    def can_move(self, x, y):
        if 0 <= x <= self.width - 25 and 0 <= y <= self.height - 25:
            for link in self.snake_body:
                if link == [x, y]:
                    return False
            return True
        return False

    def loss(self):
        self.stop_game = True
        font = pygame.font.SysFont('gothic', 80)
        text = font.render('Game over', True, (255, 0, 0))
        text_x = self.width / 2 - text.get_width() / 2
        text_y = self.height / 2 - text.get_height() / 2
        self.screen.blit(text, (text_x, text_y))
        self.draw_statistics(text_y)
        self.change_apple_coordinates()

    def change_direction(self, new_direction):
        if new_direction == 0 and self.direction != 2:
            self.direction = 0
        elif new_direction == 1 and self.direction != 3:
            self.direction = 1
        elif new_direction == 2 and self.direction != 0:
            self.direction = 2
        elif new_direction == 3 and self.direction != 1:
            self.direction = 3

    def change_apple_coordinates(self):
        self.apple.sprite.change_coordinates()
        while not self.check_apple_coordinates():
            self.apple.sprite.change_coordinates()

    def generate_apple(self):
        self.apple = Apple()

    def check_apple_coordinates(self):
        correct_coordinates = True
        for link in self.snake_body:
            if [self.apple.sprite.rect.x, self.apple.sprite.rect.y] == link:
                correct_coordinates = False
                break
        return correct_coordinates

    def check_intersection_with_apple(self):
        if [self.apple.sprite.rect.x, self.apple.sprite.rect.y] == self.snake_body[-1]:
            self.length_body += 1
            self.fps += 0.2
            self.change_apple_coordinates()

    def draw_statistics(self, y):
        font = pygame.font.SysFont('gothic', 50)
        y = y + 45
        database = sqlite3.connect('data/database.sql')
        cursor = database.cursor()
        best_result = cursor.execute('''SELECT result from statistics_in_snake 
                   WHERE id=1''').fetchone()[0]
        current_result = self.length_body - 2
        if current_result > best_result:
            best_result = current_result
            text = font.render('Новый рекорд!', True, (255, 0, 0))
            text_x = self.width / 2 - text.get_width() / 2
            self.screen.blit(text, (text_x, y))
            cursor.execute('''UPDATE statistics_in_snake
                                                   SET result = ?
                                                   WHERE id=1''', (current_result,))
            database.commit()
            y += 30
        database.close()
        font = pygame.font.SysFont('gothic', 25)
        text = font.render(f"Текущий результат: {current_result}", True, (255, 0, 0))
        text_x = self.width / 2 - text.get_width() / 2
        self.screen.blit(text, (text_x, y))
        y += 15

        text = font.render(f"Лучший результат: {best_result}", True, (255, 0, 0))
        text_x = self.width / 2 - text.get_width() / 2
        self.screen.blit(text, (text_x, y))

    def restart(self):
        self.length_body = 2
        self.snake_body = [[300, 200], [300, 225]]
        self.stop_game = False
        self.tongue_state = 0
        self.tongue_len = 7
        self.direction = 2

    def start(self):
        self.clock = pygame.time.Clock()
        self.running = True
        self.fps = 8
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if not self.stop_game:
                        if event.key in [pygame.K_d, pygame.K_RIGHT]:
                            self.change_direction(1)
                        elif event.key in [pygame.K_s, pygame.K_DOWN]:
                            self.change_direction(2)
                        elif event.key in [pygame.K_a, pygame.K_LEFT]:
                            self.change_direction(3)
                        elif event.key in [pygame.K_w, pygame.K_UP]:
                            self.change_direction(0)
                    else:
                        self.restart()
            if not self.stop_game:
                self.field.draw(self.screen)
                self.draw_snake()
                self.move_snake()
                self.apple.draw(self.screen)
                self.check_intersection_with_apple()
                self.change_tongue()
            self.clock.tick(self.fps)
            pygame.display.flip()
        pygame.quit()