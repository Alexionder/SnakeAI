import pygame


def play(snake):
    pygame.init()
    resolution = (600, 600)

    board_size = 25
    tile_size = (resolution[0] / board_size, resolution[1] / board_size)

    window = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()
    fps = 10

    red = (234, 11, 11)
    green = (11, 234, 11)
    blue = (11, 11, 234)
    white = (234, 234, 234)
    black = (11, 11, 11)
    on = True

    while on:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                on = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(0)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(1)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(2)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(3)

        window.fill(white)

        if snake.apple is not None:
            pygame.draw.rect(window,
                             red,
                             (snake.apple.x*tile_size[0], snake.apple.y*tile_size[1], tile_size[0], tile_size[1]))

        pygame.draw.rect(window,
                         green,
                         (snake.coords[0]*tile_size[0], snake.coords[1]*tile_size[1], tile_size[0], tile_size[1]))

        for tile in snake.tail:
            pygame.draw.rect(window,
                             green,
                             (tile[0] * tile_size[0], tile[1] * tile_size[1], tile_size[0], tile_size[1]))

        if snake.apple is not None:
            pygame.draw.rect(window,
                             red,
                             (snake.apple.x * tile_size[0], snake.apple.y * tile_size[1], tile_size[0], tile_size[1]),
                             1)

        if snake.alive:
            snake.move()

        pygame.display.update()
        clock.tick(fps)
    pygame.quit()
