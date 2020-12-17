import pygame


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 0
        self.top = 0
        self.cell_size = 50

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, screen):
        for i in range(self.height):
            for j in range(self.width):
                x, y = self.get_cell_position(i, j)
                rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(screen, pygame.Color('white'),
                                 rect, width=1)

    def get_cell_position(self, i, j):
        x = j * self.cell_size + self.left
        y = i * self.cell_size + self.top
        return x, y


if __name__ == '__main__':
    board = Board(5, 7)
    running = True
    screen = pygame.display.set_mode((800, 800))
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        board.render(screen)
        pygame.display.flip()