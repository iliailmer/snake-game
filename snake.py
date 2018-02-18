import pygame
import sys
from pygame.locals import *
import random
import keyboard

random.seed(4242)

class Snake:
    def __init__(self, cellwidth, cellheight):
        self._startX = random.randint(5, cellwidth - 6)
        self._startY = random.randint(5, cellheight - 6)
        self.coord = [{'x': self._startX, 'y': self._startY},
                      {'x': self._startX - 1, 'y': self._startY},
                      {'x': self._startX - 2, 'y': self._startY}]

    def UP(self):
        keyboard.press_and_release('w')
        self.coord.insert(0, {'x': self.coord[0]['x'], 'y': self.coord[0]['y'] - 1})
        del self.coord[-1]
        # direction = UP

    def DOWN(self):
        keyboard.press_and_release('s')
        self.coord.insert(0, {'x': self.coord[0]['x'], 'y': self.coord[0]['y'] + 1})
        del self.coord[-1]
        # direction = DOWN

    def RIGHT(self):
        keyboard.press_and_release('d')
        self.coord.insert(0, {'x': self.coord[0]['x'] + 1, 'y': self.coord[0]['y']})
        del self.coord[-1]
        # direction = RIGHT

    def LEFT(self):
        keyboard.press_and_release('a')
        self.coord.insert(0, {'x': self.coord[0]['x'] - 1, 'y': self.coord[0]['y']})
        del self.coord[-1]
        # direction = LEFT


class GameLogic:
    def __init__(self):
        self.WIDTH = 800
        self.HEIGHT = 600

        self.CELLSIZE = 20
        self.CELLWIDTH = int(self.WIDTH / self.CELLSIZE)
        self.CELLHEIGHT = int(self.HEIGHT / self.CELLSIZE)

        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.DARKGREEN = (0, 155, 0)
        self.DARKGRAY = (40, 40, 40)
        self.BGCOLOR = self.BLACK

        self.UP = 'up'
        self.DOWN = 'down'
        self.LEFT = 'left'
        self.RIGHT = 'right'

        self.dirList = [self.UP, self.DOWN, self.LEFT, self.RIGHT]
        self.direction = None

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

    def metApple(self, snake, apple):
        if snake.coord[0]['x'] == apple['x'] and snake.coord[0]['y'] == apple['y']:
            return True
        else:
            return False

    def makeApple(self):
        apple = {'x': random.randint(0, self.CELLWIDTH - 1), 'y': random.randint(0, self.CELLHEIGHT - 1)}
        return apple

    def randomDirection(self):
        dir_index = random.randint(0, 3)
        return self.Directions[dir_index]

    def runGame(self, snake):
        apple = self.makeApple()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.terminate()
                elif event.type == KEYDOWN:
                    if (event.key == K_LEFT or event.key == K_a) and self.direction != self.RIGHT:
                        if self.metApple(snake, apple):
                            apple = self.makeApple()
                            snake.coord.insert(len(snake.coord) - 1,
                                         {'x': apple['x'] + snake.coord[0]['x'], 'y': apple['y'] + snake.coord[0]['y']})
                        else:
                            snake.LEFT()
                            self.direction = self.LEFT
                    elif (event.key == K_RIGHT or event.key == K_a) and self.direction != self.RIGHT:



