################################################################################
##                                                                            ##
##  Copyright (C) 2015 Mohd Tarmizi Mohd Affandi                              ##
##                                                                            ##
################################################################################

import pyglet
from pyglet.window import key
from collections import deque
import random

window = pyglet.window.Window()
spritesheet = pyglet.resource.image('sprites.png')
rows = [
    'BODY_R',
    'BODY_D',
    'BODY_L',
    'BODY_U',
    'TAIL_R',
    'TAIL_D',
    'TAIL_L',
    'TAIL_U',
    'HEAD_R',
    'HEAD_D',
    'HEAD_L',
    'HEAD_U',
    'BODY_RD',
    'BODY_DL',
    'BODY_LU',
    'BODY_UR',
    'BODY_UL',
    'BODY_RU',
    'BODY_DR',
    'BODY_LD',
    'TAIL_RD',
    'TAIL_DL',
    'TAIL_LU',
    'TAIL_UR',
    'TAIL_UL',
    'TAIL_RU',
    'TAIL_DR',
    'TAIL_LD',
    'HEAD_RD',
    'HEAD_DL',
    'HEAD_LU',
    'HEAD_UR',
    'HEAD_UL',
    'HEAD_RU',
    'HEAD_DR',
    'HEAD_LD',
    'APPLE',
]
sprites = {}
for (row, name) in enumerate(rows):
    sprites[name] = [
        spritesheet.get_region(
            x = 16 * col,
            y = 592 - (16 * row) - 16,
            width = 16,
            height = 16
        )
        for col in range(16)
    ]

class Arena:
    def __init__(self):
        self.timestamp = 0
        self.dimensions = (40, 30)
        self.speed = 8
        self.new_snake()        
        self.new_apple()

    def set_direction(self, direction):
        opposites = {'D': 'U', 'U': 'D', 'L': 'R', 'R': 'L'}
        (x, y, head_direction) = self.snake[-1]
        if opposites[head_direction] == direction:
            pass # Deny, perhaps with a visual indicator or a sound effect
        else:
            self.direction = direction

    def new_snake(self):
        self.snake = deque([
            (0, 0, 'R'),
            (1, 0, 'R'),
            (2, 0, 'R'),
            (3, 0, 'R'),
            (4, 0, 'R'),
        ])
        self.collision = -1
        self.grow = False
        self.direction = 'R'

    def new_apple(self):
        self.apple = (random.randrange(0, self.dimensions[0]), random.randrange(0, self.dimensions[1]))
        if self.apple in [(x, y) for (x, y, direction) in self.snake]:
            self.new_apple()

    def segments(self):
        return [(x, y) for (x, y, direction) in self.snake]

    def update(self, dt):
        old_tick = int(self.timestamp * self.speed)
        self.timestamp += dt
        new_tick = int(self.timestamp * self.speed)
        if self.collision >= 0:
            return
        (width, height) = self.dimensions
        for tick in range(old_tick, new_tick):
            if not self.grow:
                self.snake.popleft()
            (x, y, direction) = self.snake[-1]
            if self.direction == 'R':
                x = (x + 1) % width
            elif self.direction == 'L':
                x = (x - 1) % width
            elif self.direction == 'U':
                y = (y + 1) % height
            elif self.direction == 'D':
                y = (y - 1) % height
            if (x, y) in self.segments()[1:]:
                self.collision = tick
            else:
                self.snake.append((x, y, self.direction))
                if self.apple == (x, y):
                    self.grow = True
                    self.new_apple()
                else:
                    self.grow = False

    def draw(self):
        frame = int(self.timestamp * self.speed * 16) % 16
        if self.collision >= 0 and self.collision < int(self.timestamp * self.speed):
            frame = 15

        batch = pyglet.graphics.Batch()
        s = []

        # Draw apple
        (x, y) = self.apple
        s.append(pyglet.sprite.Sprite(sprites['APPLE'][frame], x = x * 16, y = y * 16, batch = batch))

        # Draw snake
        for (i, (x, y, direction)) in enumerate(self.snake): # TODO: Batch
            part = 'BODY'
            if i == 0:
                part = 'TAIL'
            elif i == len(self.snake) - 1:
                part = 'HEAD'
            if len(self.snake) > (i + 1) and self.snake[i + 1][2] != direction:
                direction += self.snake[i + 1][2]
            elif len(self.snake) == (i + 1) and self.direction != direction:
                direction += self.direction
            name = '{}_{}'.format(part, direction)
            if name in sprites:
                if self.grow and i == 0:
                    img = sprites[name][0]
                else:
                    img = sprites[name][frame]
                s.append(pyglet.sprite.Sprite(img, x = x * 16, y = y * 16, batch = batch))

        batch.draw()

arena = Arena()

@window.event
def on_key_press(symbol, modifiers):
    keymap = {key.UP: 'U', key.DOWN: 'D', key.LEFT: 'L', key.RIGHT: 'R'}
    if symbol in keymap:
        arena.set_direction(keymap[symbol])
    if symbol == key.SPACE and arena.collision >= 0:
        arena.new_snake()
        arena.new_apple()

@window.event
def on_draw():
    window.clear()
    arena.draw()

def main():
    pyglet.clock.schedule_interval(arena.update, 1.0 / 32)
    pyglet.app.run()

if __name__ == '__main__':
    main()
