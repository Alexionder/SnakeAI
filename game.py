import pygame


def get_tile_rects(snake, index, tile_size, edge_size):
    rects = []
    for neighbor in [snake[index - 1] if index > 0 else None, snake[index + 1] if index < len(snake) - 1 else None]:
        if neighbor is not None:
            xoff = edge_size
            yoff = edge_size
            width_off = -edge_size * 2
            height_off = -edge_size * 2
            direction = (neighbor[0] - snake[index][0], neighbor[1] - snake[index][1])
            if direction == (0, -1):
                yoff = 0
                height_off += edge_size
            elif direction == (1, 0):
                width_off = 0
            elif direction == (0, 1):
                height_off = 0
            elif direction == (-1, 0):
                xoff = 0
                width_off += edge_size
            rects.append((snake[index][0] * tile_size[0] + xoff,
                          snake[index][1] * tile_size[1] + yoff,
                          tile_size[0] + width_off,
                          tile_size[1] + height_off))
    return rects


def play(snake, hold=True):
    pygame.init()
    resolution = (600, 600)

    tile_size = (resolution[0] / snake.bounds[0], resolution[1] / snake.bounds[1])

    window = pygame.display.set_mode(resolution)
    clock = pygame.time.Clock()
    fps = 25

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
                    snake.change_orientation(0)
                elif event.key == pygame.K_RIGHT:
                    snake.change_orientation(1)
                elif event.key == pygame.K_DOWN:
                    snake.change_orientation(2)
                elif event.key == pygame.K_LEFT:
                    snake.change_orientation(3)

        window.fill(white)

        if snake.apple is not None:
            pygame.draw.rect(window,
                             red,
                             (snake.apple.x * tile_size[0], snake.apple.y * tile_size[1], tile_size[0], tile_size[1]))

        for tile, i in zip(snake.tail[:] + [snake.pos], range(len(snake.tail)+1)):
            for rect in get_tile_rects(snake.tail[:] + [snake.pos], i, tile_size, 2):
                pygame.draw.rect(window, green, rect)

        trace = [[snake.pos[0] * tile_size[0] + int(tile_size[0] / 2),
                  snake.pos[1] * tile_size[1] + int(tile_size[1] / 2)]]
        for line in snake.path:
            trace.append(
                [line[0] * tile_size[0] + int(tile_size[0] / 2), line[1] * tile_size[0] + int(tile_size[1] / 2)])
        if len(trace) > 0:
            pygame.draw.polygon(window, blue, trace + trace[::-1], 1)



        pygame.display.update()
        if snake.alive:
            snake.ping_to_move()
        elif not hold:
            on = False
        # clock.tick(fps)
    pygame.quit()


def play_no_visual(snake):
    while snake.alive:
        snake.ping_to_move()
