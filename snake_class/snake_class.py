import pygame
import sys
from pygame.locals import *
import random

random.seed(42)


class SnakeGame:
    def __init__(self, width, height):
        self.WIDTH = width
        self.HEIGHT = height

        self.CELLWIDTH = int(self.WIDTH / self.CELLSIZE)
        self.CELLHEIGHT = int(self.HEIGHT / self.CELLSIZE)
        self.CELLSIZE = 20

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.DARKGREEN = (0, 155, 0)
        self.DARKGRAY = (40, 40, 40)
        self.BGCOLOR = self.BLACK

        self.GameOver = True

        self.CLOCK = pygame.time.Clock()
        self.DISPLAY = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

        self.UP = 'up'
        self.DOWN = 'down'
        self.LEFT = 'left'
        self.RIGHT = 'right'

        self.actions = {
            0: K_w,
            1: K_a,
            2: K_d,
            3: K_s
        }

    def main(self):
        pygame.init()
        pygame.display.set_caption('Snake')

        while True:
            if self.GameOver:
                self.runGame()

    def terminate(self):
        pygame.quit()
        sys.exit()

    def checkPressedKey(self):
        if len(pygame.event.get(QUIT)) > 0:
            self.terminate()

        keyUpEvents = pygame.event.get(KEYUP)
        if len(keyUpEvents) == 0:
            return None
        if keyUpEvents[0].key == K_ESCAPE:
            self.terminate()
        return keyUpEvents[0].key

    def runGame(self):
        startX = random.randint(5, self.CELLWIDTH - 6)
        startY = random.randint(5, self.CELLHEIGHT - 6)
        snake = [{'x': startX, 'y': startY},
                 {'x': startX - 1, 'y': startY},
                 {'x': startX - 2, 'y': startY}]

        apple = {'x': random.randint(0, self.CELLWIDTH - 1), 'y': random.randint(0, self.CELLHEIGHT - 1)}
        direction = None
        # main game loop goes here
        while True:
            self.GameOver = False
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYDOWN:
                    key = event.key
                    if (key == self.action[0]) and direction != self.RIGHT:
                        if self.metApple(snake, apple):
                            apple = {'x': random.randint(0, self.CELLWIDTH - 1),
                                     'y': random.randint(0, self.CELLHEIGHT - 1)}
                            snake.insert(len(snake) - 1, {'x': apple['x'] + snake[0]['x'],
                                                          'y': apple['y'] + snake[0]['y']})
                        else:
                            direction = self.LEFT
                            snake.insert(0, {'x': snake[0]['x'] - 1, 'y': snake[0]['y']})
                            del snake[-1]
                    elif (key == self.action["right"]) and direction != self.LEFT:
                        if self.metApple(snake, apple):
                            apple = {'x': random.randint(0, self.CELLWIDTH - 1),
                                     'y': random.randint(0, self.CELLHEIGHT - 1)}
                            snake.insert(len(snake) - 1,
                                         {'x': apple['x'] + snake[0]['x'], 'y': apple['y'] + snake[0]['y']})
                        else:
                            direction = self.RIGHT
                            snake.insert(0, {'x': snake[0]['x'] + 1, 'y': snake[0]['y']})
                            del snake[-1]
                    elif (key == self.action["up"]) and direction != self.DOWN:
                        if self.metApple(snake, apple):
                            apple = {'x': random.randint(0, self.CELLWIDTH - 1),
                                     'y': random.randint(0, self.CELLHEIGHT - 1)}
                            snake.insert(len(snake) - 1, {'x': apple['x'] + snake[0]['x'],
                                                          'y': apple['y'] + snake[0]['y']})
                        else:
                            direction = self.UP
                            snake.insert(0, {'x': snake[0]['x'], 'y': snake[0]['y'] - 1})
                            del snake[-1]
                    elif (key == self.action["down"]) and direction != self.UP:
                        if self.metApple(snake, apple):
                            apple = {'x': random.randint(0, self.CELLWIDTH - 1),
                                     'y': random.randint(0, self.CELLHEIGHT - 1)}
                            snake.insert(len(snake) - 1, {'x': apple['x'] + snake[0]['x'],
                                                          'y': apple['y'] + snake[0]['y']})
                        else:
                            direction = self.DOWN
                            snake.insert(0, {'x': snake[0]['x'], 'y': snake[0]['y'] + 1})
                            del snake[-1]
                    elif event.key == K_ESCAPE:
                        self.terminate()

            # check if the snake hit the edge
            if snake[0]['x'] == -1 or snake[0]['x'] == self.CELLWIDTH or snake[0]['y'] == -1 or snake[0]['y'] == self.CELLHEIGHT:
                self.GameOver = True
                return
            # check if hits itself
            for wormBody in snake[1:]:
                if wormBody['x'] == snake[0]['x'] and wormBody['y'] == snake[0]['y']:
                    self.GameOver = True
                    return

            self.DISPLAY.fill(self.BGCOLOR)
            self.drawGrid()
            self.drawWorm(snake)
            self.drawApple(apple)
            self.drawScore(len(snake) - 3)
            pygame.display.update()
            self.CLOCK.tick(15)

    def drawGrid(self):
        for x in range(0, self.WIDTH, self.CELLSIZE):
            pygame.draw.line(self.DISPLAY, self.DARKGRAY, (x, 0), (x, self.HEIGHT))
        for y in range(0, self.HEIGHT, self.CELLSIZE):
            pygame.draw.line(self.DISPLAY, self.DARKGRAY, (0, y), (self.WIDTH, y))

    def drawWorm(self, coords):
        for coord in coords:
            x = coord['x'] * self.CELLSIZE
            y = coord['y'] * self.CELLSIZE
            wormSegmentRect = pygame.Rect(x, y, self.CELLSIZE, self.CELLSIZE)
            pygame.draw.rect(self.DISPLAY, self.DARKGREEN, wormSegmentRect)
            wormInnerSegmentRect = pygame.Rect(x + 4, y + 4, self.CELLSIZE - 8, self.CELLSIZE - 8)
            pygame.draw.rect(self.DISPLAY, self.GREEN, wormInnerSegmentRect)

    def drawApple(self, coord):
        x = coord['x'] * self.CELLSIZE
        y = coord['y'] * self.CELLSIZE
        appleRect = pygame.Rect(x, y, self.CELLSIZE, self.CELLSIZE)
        pygame.draw.rect(self.DISPLAY, self.ED, appleRect)

    def drawScore(self, score):
        scoreSurf = self.BASICFONT.render('Score: %s' % score, True, self.WHITE)
        scoreRect = scoreSurf.get_rect()
        scoreRect.topleft = (self.WIDTH - 120, 10)
        self.DISPLAY.blit(scoreSurf, scoreRect)

    def finishGame(self):
        pressKeySurf = self.BASICFONT.render('Press any key to play.', True, self.DARKGRAY)
        pressKeyRect = pressKeySurf.get_rect()
        pressKeyRect.topleft = (self.WIDTH - 200, self.HEIGHT - 30)
        self.DISPLAY.blit(pressKeySurf, pressKeyRect)
        pygame.display.update()
        pygame.time.wait(500)
        self.checkPressedKey()
        while True:
            if self.checkPressedKey():
                pygame.event.get()
                return

    def metApple(self, snake, apple):
        if snake[0]['x'] == apple['x'] and snake[0]['y'] == apple['y']:
            return True
        else:
            return False
