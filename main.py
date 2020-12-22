import pygame
from Tetris import Tetris
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('')
    width, height = 750, 900
    size = width, height
    screen = pygame.display.set_mode(size)
    clock = pygame.time.Clock()
    fps = 60
    running = True
    game = Tetris(fps, screen)
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                game.on_key_pressed(event.key, screen)
            if event.type == pygame.MOUSEBUTTONDOWN:
                game.get_click(event.pos)
        screen.fill(pygame.Color('gray'))
        game.render(screen)
        game.draw_buttons(screen)
        game.update(screen)
        pygame.display.flip()
        clock.tick(fps)
    pygame.quit()
