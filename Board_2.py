import pygame


class Board:
    def __init__(self, width, height, left=10, top=10, cell_size=30, default_value=0):
        self.width = width
        self.height = height
        self.default_value = default_value
        self.board = self.generate_board()
        self.set_view(left, top, cell_size)
        self.border_color = pygame.Color('white')
        self.border_width = 1

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def generate_board(self):
        return [[self.default_value] * self.width for _ in range(self.height)]

    def set_full_board(self, board):
        self.board = board

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                self.render_cell(i, j, screen)

    def render_cell(self, i, j, screen):
        x, y = self.get_cell_position(i, j)
        rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        pygame.draw.rect(screen, self.border_color, rect, width=self.border_width)

    def get_cell_position(self, i, j):
        x = j * self.cell_size + self.left
        y = i * self.cell_size + self.top
        return x, y

    def get_column(self, i):
        row = []
        for j in range(self.width):
            row.append((i, j))
        return row

    def get_row(self, j):
        column = []
        for i in range(self.height):
            column.append((i, j))
        return column

    def get_neighbors(self, row, col, connect_borders=False):
        result = []
        for i in range(row - 1, row + 2):
            for j in range(col - 1, col + 2):
                if i == row and j == col:
                    continue
                result.append((i, j))
        return list(
            filter(lambda pos: pos, map(lambda pos: self.get_neighbors_check_position(pos, connect_borders), result)))

    def get_neighbors_check_position(self, position, connect_borders):
        i, j = position
        if connect_borders:
            if i < 0:
                i = self.height - 1
            if j < 0:
                j = self.width - 1
            if i >= self.height:
                i = 0
            if j >= self.width:
                j = 0
            return i, j
        else:
            if i < 0:
                return None
            elif j < 0:
                return None
            elif i == self.height:
                return None
            elif j == self.width:
                return None
            return i, j

    def get_cell(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        for i in range(self.height):
            for j in range(self.width):
                x, y = self.get_cell_position(i, j)
                if x < mouse_x < x + self.cell_size and y < mouse_y < y + self.cell_size:
                    return i, j
        return None

    def on_click(self, cell_coords):
        pass

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell is not None:
            self.on_click(cell)
