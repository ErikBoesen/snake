from pygame.locals import *
import random
import pygame
import time

STEP   = 20
WIDTH  = 10
HEIGHT = 10

class Apple:
    x = 0
    y = 0

    def place(self):
        self.x = random.randint(0, WIDTH)
        self.y = random.randint(0, HEIGHT)
        print('Apple: %d %d' % (self.x, self.y))

class Segment:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    segments = []
    speed_x = 0
    speed_y = 0

    def __init__(self, x, y):
        self.segments.append(Segment(x, y))

    def set_speed(self, x, y):
        if (not ((-x == self.speed_x) and (-y == self.speed_y))) or (len(self.segments) == 1):
            self.speed_x = x
            self.speed_y = y

    def move(self):
        self.segments[0].x += self.speed_x
        self.segments[0].y += self.speed_y
        for i in range(len(self.segments), 1, -1):
            self.segments[i].x = self.segments[i - 1].x
            self.segments[i].y = self.segments[i - 1].y

    def grow(self):
        tail = self.segments[-1]
        self.segments.append(Segment(tail.x + self.speed_x, tail.y + self.speed_y))

    def looped(self):
        for segment in self.segments[1:]:
            if segment.x == self.segments[0].x and segment.y == self.segments[0].y:
                return True
        return False

    # TODO: Implement ate method here?

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)
GREEN = (  0, 255,   0)
RED =   (255,   0,   0)
class App:
    # TODO: Move actual game logic to Game object
    snake = Snake(1, 1)
    apple = Apple()

    def __init__(self):
        self.running = True

    def on_init(self):
        pygame.init()
        self.surface = pygame.display.set_mode((WIDTH * STEP, HEIGHT * STEP))
        pygame.display.set_caption('Snake')
        self.running = True

    def on_event(self, event):
        if event.type == QUIT:
            self.running = False

    def on_loop(self):
        self.snake.move()
        # TODO: Move self logic to snake
        if self.snake.segments[0].x == self.apple.x and self.snake.segments[0].y == self.apple.y:
            self.apple.place()
            self.snake.grow()

        if not (0 <= self.snake.segments[0].x < WIDTH and 0 <= self.snake.segments[0].y < HEIGHT) or self.snake.looped():
            print(len(self.snake.segments))
            # TODO: Reset game rather than quitting
            self.running = False

    def on_render(self):
        self.surface.fill(BLACK)
        pygame.draw.rect(self.surface, RED, [self.apple.x * STEP, (HEIGHT - self.apple.y) * STEP, STEP, STEP])
        for segment in self.snake.segments:
            pygame.draw.rect(self.surface, GREEN, [segment.x * STEP, (HEIGHT - segment.y) * STEP, STEP, STEP])
        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self.running = False
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

            self.on_loop()
            self.on_render()

            time.sleep(0.1)
        self.on_cleanup()

if __name__ == '__main__':
    App().on_execute()
