import pygame
from Cell import Cells
from random import randrange
from Smiley import Smiley


class Minesweeper():
    def __init__(self, mines_count, count_cells):
        pygame.init()
        pygame.display.set_caption('Minesweeper')
        self.CELL_SIZE = 30
        self.mines_count = mines_count
        self.flag_count = mines_count
        self.time = 0
        self.first_action = True
        self.stop_game = False
        self.width = self.CELL_SIZE * count_cells[0]
        self.height = self.CELL_SIZE * count_cells[1] + 40
        self.size = self.width, self.height
        self.screen = pygame.display.set_mode(self.size)
        self.screen.fill(pygame.Color((180, 180, 180)))
        self.count_cells = count_cells
        self.smiley = Smiley(self.width)
        self.create_board()

    def render(self):
        for i in range(self.count_cells[1]):
            y = i * self.CELL_SIZE + 40
            for j in range(self.count_cells[0]):
                x = j * 30
                pygame.draw.rect(self.screen, pygame.Color('black'),
                                 pygame.Rect((x, y), (self.CELL_SIZE, self.CELL_SIZE)), width=1)
        self.draw_flag_count()
        self.draw_time()
        self.draw_smiley()

    def draw_flag_count(self):
        width = 60
        height = 40
        pygame.draw.rect(self.screen, pygame.Color('black'),
                         pygame.Rect((0, 0), (width, height)))
        font = pygame.font.SysFont('Gothic', 30)
        text = font.render(str(self.flag_count).rjust(2, '0'), True, (255, 0, 0))
        text_x = width // 2 - text.get_width() // 2
        text_y = height // 2 - text.get_height() // 2
        self.screen.blit(text, (text_x, text_y))

    def draw_time(self):
        width = 60
        height = 40
        x = self.screen.get_width() - width
        y = 0
        pygame.draw.rect(self.screen, pygame.Color('black'),
                         pygame.Rect((x, y), (width, height)))
        font = pygame.font.SysFont('Gothic', 30)
        text = font.render(str(self.time).rjust(3, '0'), True, (255, 0, 0))
        text_x = (width // 2 - text.get_width() // 2) + x
        text_y = abs(y // 2 - text.get_height() // 2)
        self.screen.blit(text, (text_x, text_y))

    def draw_smiley(self):
        self.smiley.update()
        self.smiley.draw(self.screen)
        pygame.draw.rect(self.screen, pygame.Color('black'),
                         pygame.Rect((self.smiley.sprite.rect.x, self.smiley.sprite.rect.y),
                                     (self.smiley.sprite.rect.width, self.smiley.sprite.rect.height)), width=1)

    def create_board(self):
        self.board = []
        for row in range(self.count_cells[1]):
            line = Cells(self.count_cells[0], row)
            self.board.append(line)

    def place_mines(self, exception):
        current_mines = 0
        while current_mines < self.mines_count:
            cell = self.board[randrange(0, self.count_cells[1])].sprites()[randrange(0, self.count_cells[0])]
            if cell != exception and cell.condition != -2:
                cell.condition = -2
                current_mines += 1
        self.first_action = False
        self.open_cell(exception)

    def open_cell(self, cell):
        if cell == None:
            return
        if cell.condition == -2:
            cell.rect.x += 1
            cell.rect.y += 1
            cell.condition = 15
            self.loss()
        elif cell.condition == -1:
            cell.condition = 1
            cell.rect.x += 1
            cell.rect.y += 1
            neighbors = self.get_neighbors(cell.row, cell.column)
            mines_around = 0
            for neighbor in neighbors:
                if neighbor.condition in [-2, 13, 14, 15]:
                    mines_around += 1
            if mines_around:
                cell.mines_around = mines_around
            else:
                for neighbor in neighbors:
                    if neighbor.condition != -2:
                        self.open_cell(neighbor)
        elif cell.condition == 1:
            neighbors = self.get_neighbors(cell.row, cell.column)
            mines_around = 0
            flag_around = 0
            for neighbor in neighbors:
                if neighbor.condition == -2:
                    mines_around += 1
                elif neighbor.condition == 12:
                    flag_around += 1
            if not mines_around:
                for neighbor in neighbors:
                    if neighbor.condition not in [-2, 1]:
                        self.open_cell(neighbor)
            else:
                if mines_around == flag_around:
                    for neighbor in neighbors:
                        if neighbor.condition == -2:
                            neighbor.condition = 15
                    self.loss()

    def loss(self):
        self.open_board()
        self.stop_game = True
        self.smiley.sprite.state = 0

    def victory(self):
        self.stop_game = True
        self.smiley.sprite.state = 1

    def open_board(self):
        for row in self.board:
            for cell in row.sprites():
                if cell.condition == -1:
                    self.open_cell(cell)
                elif cell.condition == -2:
                    cell.condition = 14
                    cell.rect.x += 1
                    cell.rect.y += 1
                elif cell.condition == 12:
                    cell.condition = 16

    def get_neighbors(self, row_cell, column_cell):
        neighbors = []
        for row in range(row_cell - 1, row_cell + 2):
            for column in range(column_cell - 1, column_cell + 2):
                if 0 <= row <= self.count_cells[1] - 1 and 0 <= column <= self.count_cells[0] - 1:
                    if row != row_cell or column != column_cell:
                        neighbors.append(self.board[row].sprites()[column])
        return neighbors

    def cell_search(self, position):
        for line in self.board:
            for cell in line:
                if cell.rect.collidepoint(position):
                    return cell

    def set_flag(self, cell):
        if cell == None:
            return
        if cell.condition == -2:
            cell.condition = 13
            self.flag_count -= 1
        elif cell.condition == -1:
            cell.condition = 12
            self.flag_count -= 1
        elif cell.condition == 12:
            cell.condition = -1
            self.flag_count += 1
        elif cell.condition == 13:
            cell.condition = -2
            self.flag_count += 1

    def restart(self):
        self.create_board()
        self.first_action = True
        self.smiley.sprite.state = 2
        self.stop_game = False
        self.flag_count = self.mines_count
        self.time = 0

    def checking_remaining_cells(self):
        close_cells = []
        for row in range(self.count_cells[1]):
            for column in range(self.count_cells[0]):
                cell = self.board[row].sprites()[column]
                if cell.condition == -2:
                   close_cells.append(cell)
                elif cell.condition == -1:
                    return None
        return close_cells

    def start(self):
        fps = 60
        clock = pygame.time.Clock()
        self.running = True
        self.MYEVENTTYPE = pygame.USEREVENT + 1
        pygame.time.set_timer(self.MYEVENTTYPE, 1000)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if not self.stop_game:
                    close_cells = self.checking_remaining_cells()
                    if close_cells != None and len(close_cells) == self.flag_count:
                        for cell in close_cells:
                            self.set_flag(cell)
                    if self.flag_count == 0:
                        win = True
                        for row in range(self.count_cells[1]):
                            for column in range(self.count_cells[0]):
                                if self.board[row].sprites()[column].condition == -2 or\
                                        self.board[row].sprites()[column].condition == -1:
                                    win = False
                                    break
                        if win:
                            self.victory()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 3:
                            self.set_flag(self.cell_search(event.pos))
                        elif event.button == 1:
                            if self.first_action:
                                self.place_mines(self.cell_search(event.pos))
                            else:
                                self.open_cell(self.cell_search(event.pos))
                    if event.type == self.MYEVENTTYPE and not self.first_action:
                        self.time += 1
                else:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            if self.smiley.sprite.rect.collidepoint(event.pos):
                                self.restart()
            pygame.display.flip()
            clock.tick(fps)
            self.render()
            for line in self.board:
                line.update()
                line.draw(self.screen)
        pygame.quit()
