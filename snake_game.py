import pygame
import sys
from pygame.locals import *
import random

WIDTH = 800
HEIGHT = 600

CELLSIZE = 20
CELLWIDTH = int(WIDTH / CELLSIZE)
CELLHEIGHT = int(HEIGHT / CELLSIZE)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 155, 0)
DARKGRAY = (40, 40, 40)
BGCOLOR = BLACK

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def main():
    global DISPLAY, CLOCK, BASICFONT
    pygame.init()
    CLOCK = pygame.time.Clock()
    DISPLAY = pygame.display.set_mode((WIDTH, HEIGHT))
    BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
    pygame.display.set_caption('Snake')

    gameScreen()
    while True:
        runGame()
        finishGame()


def gameScreen():
    DISPLAY.fill(BGCOLOR)
    while True:
        pressKeySurf = BASICFONT.render('Press any key to play.', True, DARKGRAY)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.topleft = (WIDTH - 200, HEIGHT - 30)
        DISPLAY.blit(pressKeySurf, pressKeyRect)

        if checkPressedKey():
            pygame.event.get()
            return
        pygame.display.update()
        CLOCK.tick(15)


def terminate():
    pygame.quit()
    sys.exit()


def checkPressedKey():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()

    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key


def runGame():
    startX = random.randint(5, CELLWIDTH - 6)
    startY = random.randint(5, CELLHEIGHT - 6)
    snake = [{'x': startX, 'y': startY},
             {'x': startX - 1, 'y': startY},
             {'x': startX - 2, 'y': startY}]

    apple = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
    direction = None
    # main game loop goes here
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if (event.key == K_LEFT or event.key == K_a) and direction != RIGHT:
                    if metApple(snake, apple):
                        apple = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
                        snake.insert(len(snake)-1, {'x': apple['x']+snake[0]['x'], 'y': apple['y']+snake[0]['y']})
                    else:
                        direction = LEFT
                        snake.insert(0, {'x': snake[0]['x'] - 1, 'y': snake[0]['y']})
                        del snake[-1]
                elif (event.key == K_RIGHT or event.key == K_d) and direction != LEFT:
                    if metApple(snake, apple):
                        apple = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
                        snake.insert(len(snake) - 1, {'x': apple['x'] + snake[0]['x'], 'y': apple['y'] + snake[0]['y']})
                    else:
                        direction = RIGHT
                        snake.insert(0, {'x': snake[0]['x'] + 1, 'y': snake[0]['y']})
                        del snake[-1]
                elif (event.key == K_UP or event.key == K_w) and direction != DOWN:
                    if metApple(snake, apple):
                        apple = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
                        snake.insert(len(snake) - 1, {'x': apple['x'] + snake[0]['x'], 'y': apple['y'] + snake[0]['y']})
                    else:
                        direction = UP
                        snake.insert(0, {'x': snake[0]['x'], 'y': snake[0]['y'] - 1})
                        del snake[-1]
                elif (event.key == K_DOWN or event.key == K_s) and direction != UP:
                    if metApple(snake, apple):
                        apple = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
                        snake.insert(len(snake) - 1, {'x': apple['x'] + snake[0]['x'], 'y': apple['y'] + snake[0]['y']})
                    else:
                        direction = DOWN
                        snake.insert(0, {'x': snake[0]['x'], 'y': snake[0]['y'] + 1})
                        del snake[-1]
                elif event.key == K_ESCAPE:
                    terminate()

        # check if the snake hit the edge
        if snake[0]['x'] == -1 or snake[0]['x'] == CELLWIDTH or snake[0]['y'] == -1 or snake[0]['y'] == CELLHEIGHT:
            return
        # check if hits itself
        for wormBody in snake[1:]:
            if wormBody['x'] == snake[0]['x'] and wormBody['y'] == snake[0]['y']:
                return

        # snake arrives at apple
        # if snake[0]['x'] == apple['x'] and snake[0]['y'] == apple['y']:
        #    apple = {'x': random.randint(0, CELLWIDTH - 1), 'y': random.randint(0, CELLHEIGHT - 1)}
        #    snake.insert(len(snake)-1, {'x': snake[0]['x'], 'y': snake[0]['y'] - 1})
        # else:
        #   del snake[-1]  # remove snakes' tail segment
        """
        if direction == UP:
            snake.insert(0, {'x': snake[0]['x'], 'y': snake[0]['y'] + 1})
            del snake[-1]
        elif direction == DOWN:
            snake.insert(0, {'x': snake[0]['x'], 'y': snake[0]['y'] - 1})
            del snake[-1]
        elif direction == LEFT:
            snake.insert(0, {'x': snake[0]['x'] - 1, 'y': snake[0]['y']})
            del snake[-1]
        elif direction == RIGHT:
            snake.insert(0, {'x': snake[0]['x'] + 1, 'y': snake[0]['y']})
            del snake[-1]
        """
        DISPLAY.fill(BGCOLOR)
        drawGrid()
        drawWorm(snake)
        drawApple(apple)
        drawScore(len(snake) - 3)
        pygame.display.update()
        CLOCK.tick(15)


def drawGrid():
    for x in range(0, WIDTH, CELLSIZE):
        pygame.draw.line(DISPLAY, DARKGRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELLSIZE):
        pygame.draw.line(DISPLAY, DARKGRAY, (0, y), (WIDTH, y))


def drawWorm(coords):
    for coord in coords:
        x = coord['x'] * CELLSIZE
        y = coord['y'] * CELLSIZE
        wormSegmentRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
        pygame.draw.rect(DISPLAY, DARKGREEN, wormSegmentRect)
        wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, CELLSIZE - 8, CELLSIZE - 8)
        pygame.draw.rect(DISPLAY, GREEN, wormInnerSegmentRect)


def drawApple(coord):
    x = coord['x'] * CELLSIZE
    y = coord['y'] * CELLSIZE
    appleRect = pygame.Rect(x, y, CELLSIZE, CELLSIZE)
    pygame.draw.rect(DISPLAY, RED, appleRect)


def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % score, True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (WIDTH - 120, 10)
    DISPLAY.blit(scoreSurf, scoreRect)


def finishGame():
    gameOverFont = pygame.font.Font('freesansbold.ttf', 150)
    gameSurf = gameOverFont.render('Game', True, WHITE)
    overSurf = gameOverFont.render('Over', True, WHITE)
    gameRect = gameSurf.get_rect()
    overRect = overSurf.get_rect()
    gameRect.midtop = (WIDTH / 2, 10)
    overRect.midtop = (WIDTH / 2, gameRect.height + 10 + 25)
    DISPLAY.blit(gameSurf, gameRect)
    DISPLAY.blit(overSurf, overRect)

    pressKeySurf = BASICFONT.render('Press any key to play.', True, DARKGRAY)
    pressKeyRect = pressKeySurf.get_rect()
    pressKeyRect.topleft = (WIDTH - 200, HEIGHT - 30)
    DISPLAY.blit(pressKeySurf, pressKeyRect)
    pygame.display.update()
    pygame.time.wait(500)
    checkPressedKey()
    while True:
        if checkPressedKey():
            pygame.event.get()
            return


def metApple(snake, apple):
    if snake[0]['x'] == apple['x'] and snake[0]['y'] == apple['y']:
        return True
    else:
        return False


if __name__ == '__main__':
    main()
