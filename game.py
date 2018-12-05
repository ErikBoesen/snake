from pygame.locals import *
import random
import pygame
import time

STEP   = 20
WIDTH  = 30
HEIGHT = 30
POPULATION_SIZE = 50

class Apple:
    x = 0
    y = 0

    def place(self):
        self.x = random.randint(0, WIDTH-1)
        self.y = random.randint(1, HEIGHT)

class Segment:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

class Snake:
    segments = []
    speed_x = 0
    speed_y = 0

    def __init__(self):
        self.segments.append(Segment(random.randint(0, WIDTH-1), random.randint(1, HEIGHT)))

    def set_speed(self, x: int, y: int):
        if (not ((-x == self.speed_x) and (-y == self.speed_y))) or (len(self.segments) == 1):
            self.speed_x = x
            self.speed_y = y

    def move(self):
        for i in range(len(self.segments) - 1, 0, -1):
            self.segments[i].x = self.segments[i - 1].x
            self.segments[i].y = self.segments[i - 1].y
        self.segments[0].x += self.speed_x
        self.segments[0].y += self.speed_y

    def grow(self):
        tail = self.segments[-1]
        self.segments.append(Segment())

    def looped(self) -> bool:
        for segment in self.segments[1:]:
            if segment.x == self.segments[0].x and segment.y == self.segments[0].y:
                return True
        return False

    def outbound(self) -> bool:
        return not (0 <= self.segments[0].x < WIDTH and 1 <= self.segments[0].y < HEIGHT + 1)

    def ate(self, apple: Apple) -> bool:
        return self.segments[0].x == apple.x and self.segments[0].y == apple.y

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE  = (  0,   0, 255)
GREEN = (  0, 255,   0)
RED   = (255,   0,   0)
class App:
    snake = Snake()
    apple = Apple()

    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode((WIDTH * STEP, HEIGHT * STEP))
        pygame.display.set_caption('Snake')
        self.running = True

    def event(self, event):
        if event.type == QUIT:
            self.running = False

    def loop(self):
        self.snake.move()
        if self.snake.ate(self.apple):
            self.apple.place()
            self.snake.grow()

        if self.snake.outbound() or self.snake.looped():
            print(len(self.snake.segments))
            # TODO: Reset game rather than quitting
            self.running = False

    def render(self):
        self.surface.fill(BLACK)
        pygame.draw.rect(self.surface, RED, [self.apple.x * STEP, (HEIGHT - self.apple.y) * STEP, STEP, STEP])
        for segment in self.snake.segments:
            pygame.draw.rect(self.surface, GREEN, [segment.x * STEP, (HEIGHT - segment.y) * STEP, STEP, STEP])
        pygame.display.flip()

    def execute(self):
        self.apple.place()

        while (self.running):
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[K_RIGHT]):
                self.snake.set_speed(1, 0)
            if (keys[K_LEFT]):
                self.snake.set_speed(-1, 0)
            if (keys[K_UP]):
                self.snake.set_speed(0, 1)
            if (keys[K_DOWN]):
                self.snake.set_speed(0, -1)
            if (keys[K_ESCAPE]):
                self.running = False

            self.loop()
            self.render()

            time.sleep(0.1)
        pygame.quit()

if __name__ == '__main__':
    App().execute()
