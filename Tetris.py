from Board_2 import Board
from Piece import Piece
from shapes import shapes
import random
import pygame


class Tetris(Board):
    def __init__(self, fps, screen):
        screen = screen
        width = 10
        height = 20
        self.total = -10
        super().__init__(width, height, left=0, top=0, cell_size=45)
        self.colors = ['red', 'blue', 'yellow', 'orange', 'pink', 'purple', 'cyan']
        self.count = 0
        self.fps = fps
        self.difficulty = 30
        self.border_color = pygame.Color('black')
        self.ACTIVE_PIECE = 1
        self.BLOCK = 11
        self.bor = Board(width, height, left=0, top=0, cell_size=45)
        self.BLOCK_COLOR = pygame.Color('darkred')
        self.create_active_piece()
        self.render_active_piece(screen)

    def render_cell(self, i, j, screen):
        x, y = self.get_cell_position(i, j)
        rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        val = self.board[i][j]
        if val == self.ACTIVE_PIECE:
            pygame.draw.rect(screen, self.ACTIVE_PIECE_COLOR, rect)
        elif val == self.BLOCK:
            pygame.draw.rect(screen, self.BLOCK_COLOR, rect)
        else:
            pygame.draw.rect(screen, self.border_color, rect, width=self.border_width)

    def update(self, screen):
        self.count += 1
        if self.count % (self.fps - self.difficulty) == 0:
            self.update_world(screen)

    def is_free(self):
        self.res = True
        for row in range(1):
            if self.BLOCK in self.board[row]:
                self.res = False
        return self.res

    def update_world(self, screen):
        if self.can_move(pygame.K_DOWN):
            self.remove_active_piece()
            self.active_piece.down()
            self.render_active_piece(screen)
        else:
            self.active_piece_to_block()
            self.check_complete_lines()
            self.create_active_piece()
            self.render_active_piece(screen)

    def active_piece_to_block(self):
        shape = self.active_piece.get_shape()
        for i in range(self.active_piece.size):
            for j in range(self.active_piece.size):
                board_row = i + self.active_piece.row
                board_column = j + self.active_piece.column
                if self.is_valid_pos(board_row, board_column):
                    shape_val = int(shape[i][j])
                    if shape_val == self.ACTIVE_PIECE:
                        self.board[board_row][board_column] = self.BLOCK

    def check_complete_lines(self):
        for row in range(self.height):
            if self.board[row].count(self.BLOCK) == self.width:
                self.delete_line(row)

    def delete_line(self, index):
        for i in range(index, 0, -1):
            self.board[i] = self.board[i - 1]
        self.board[0] = [0] * self.width
        self.total += 50

    def render_active_piece(self, screen):
        shape = self.active_piece.get_shape()
        for i in range(self.active_piece.size):
            for j in range(self.active_piece.size):
                board_row = i + self.active_piece.row
                board_column = j + self.active_piece.column
                if self.is_valid_pos(board_row, board_column):
                    shape_val = int(shape[i][j])
                    if shape_val == self.ACTIVE_PIECE:
                        self.board[board_row][board_column] = self.ACTIVE_PIECE

    def remove_active_piece(self):
        shape = self.active_piece.get_shape()
        for i in range(self.active_piece.size):
            for j in range(self.active_piece.size):
                board_row = i + self.active_piece.row
                board_column = j + self.active_piece.column
                if self.is_valid_pos(board_row, board_column):
                    shape_val = int(shape[i][j])
                    if shape_val == self.ACTIVE_PIECE:
                        self.board[board_row][board_column] = self.default_value

    def is_valid_pos(self, row, col):
        return 0 <= row < self.height and 0 <= col < self.width

    def get_random_shape(self):
        self.ACTIVE_PIECE_COLOR = pygame.Color(random.choice(self.colors))
        self.total += 10
        return random.choice(list(shapes.values()))

    def create_active_piece(self):
        self.active_piece = Piece(self.get_random_shape(), -1, 3)

    def can_move(self, direction):
        actions = {pygame.K_DOWN: self.active_piece.down, pygame.K_LEFT: self.active_piece.left,
                   pygame.K_RIGHT: self.active_piece.right, pygame.K_UP: self.active_piece.rotate}
        reverse_actions = {pygame.K_DOWN: self.active_piece.up, pygame.K_LEFT: self.active_piece.right,
                           pygame.K_RIGHT: self.active_piece.left, pygame.K_UP: self.active_piece.rotate_prev}
        result = True
        actions[direction]()
        shape = self.active_piece.get_shape()
        for i in range(self.active_piece.size):
            for j in range(self.active_piece.size):
                board_row = i + self.active_piece.row
                board_column = j + self.active_piece.column
                shape_val = int(shape[i][j])
                if not self.is_valid_pos(board_row, board_column) and shape_val == self.ACTIVE_PIECE:
                    result = False
                    break
                if not self.is_valid_pos(board_row, board_column):
                    continue
                board_val = self.board[board_row][board_column]
                if shape_val == self.ACTIVE_PIECE and board_val == self.BLOCK:
                    result = False
                    break
        reverse_actions[direction]()
        return result

    def move_action(self, action, direction, screen):
        if self.can_move(direction):
            self.remove_active_piece()
            action()
            self.render_active_piece(screen)

    def on_key_pressed(self, key, screen):
        actions = {pygame.K_DOWN: self.active_piece.down, pygame.K_LEFT: self.active_piece.left,
                   pygame.K_RIGHT: self.active_piece.right, pygame.K_UP: self.active_piece.rotate}
        if key in actions:
            self.move_action(actions[key], key, screen)

    def draw_buttons(self, screen):
        font = pygame.font.Font(None, 50)
        text = font.render(f"total: {self.total}", True, (0, 0, 0))
        screen.blit(text, (525, 50))

        font = pygame.font.Font(None, 50)
        text = font.render("Выберите", True, (0, 0, 0))
        screen.blit(text, (515, 250))

        font = pygame.font.Font(None, 50)
        text = font.render("скорость игры:", True, (0, 0, 0))
        screen.blit(text, (475, 325))

        font = pygame.font.Font(None, 50)
        text = font.render("Х1", True, (0, 0, 0))
        screen.blit(text, (475, 400))

        font = pygame.font.Font(None, 50)
        text = font.render("Х2", True, (0, 0, 0))
        screen.blit(text, (575, 400))

        font = pygame.font.Font(None, 50)
        text = font.render("Х3", True, (0, 0, 0))
        screen.blit(text, (675, 400))

        pygame.draw.rect(screen, (0, 0, 0), (470, 395,
                                             50, 50), 1)
        pygame.draw.rect(screen, (0, 0, 0), (570, 395,
                                             50, 50), 1)
        pygame.draw.rect(screen, (0, 0, 0), (670, 395,
                                             50, 50), 1)

    def is_click_button_1(self):
        self.difficulty = 30

    def is_click_button_2(self):
        self.difficulty = 40

    def is_click_button_3(self):
        self.difficulty = 50

    def get_click(self, pos):
        x = pos[0]
        y = pos[1]
        if x >= 470 and x <= 520:
            if y >= 395 and y <= 445:
                self.is_click_button_1()
        if x >= 570 and x <= 620:
            if y >= 395 and y <= 445:
                self.is_click_button_2()
        if x >= 670 and x <= 720:
            if y >= 395 and y <= 445:
                self.is_click_button_3()
