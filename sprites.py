from pygame.sprite import Sprite
from pygame import Rect
from renderer import Renderer, SpriteRegistry
from action import Frame, Action
from controls import Input, State
from pygame.math import Vector2
from random import randint
from engine import Engine
from pygame.event import post, Event
from typing import Optional
from timer import Timer


class GameObject(Sprite):
    def spawn(self) -> None:
        pass

    def is_alive(self) -> bool:
        pass

    def collide(self, other: 'GameObject') -> bool:
        pass

    def draw(self, renderer: Renderer) -> None:
        pass


class Background(Sprite):
    WIDTH = 512
    HEIGHT = 256

    def __init__(self):
        super().__init__()
        self.input: Input = None
        ''' Setup layers for scrolling '''
        self.layers = [
            {
                "y": 2048,
                "scroll_x": 0,
                "scroll_step": 0,
                "view_rect_left": None,
                "view_rect_right": None,
                "source_rect_left": None,
                "source_rect_right": None,
            },
            {
                "y": 768,
                "scroll_x": 0,
                "scroll_step": 0.5,
                "view_rect_left": None,
                "view_rect_right": None,
                "source_rect_left": None,
                "source_rect_right": None,
            },
            {
                "y": 1792,
                "scroll_x": 0,
                "scroll_step": 0.5,
                "view_rect_left": None,
                "view_rect_right": None,
                "source_rect_left": None,
                "source_rect_right": None,
            },
            {
                "y": 1536,
                "scroll_x": 0,
                "scroll_step": 0.5,
                "view_rect_left": None,
                "view_rect_right": None,
                "source_rect_left": None,
                "source_rect_right": None,
            },
            {
                "y": 1024,
                "scroll_x": 0,
                "scroll_step": 1,
                "view_rect_left": None,
                "view_rect_right": None,
                "source_rect_left": None,
                "source_rect_right": None,
            },
            {
                "y": 1280,
                "scroll_x": 0,
                "scroll_step": 1,
                "view_rect_left": None,
                "view_rect_right": None,
                "source_rect_left": None,
                "source_rect_right": None,
            },
            {
                "y": 512,
                "scroll_x": 0,
                "scroll_step": 1,
                "view_rect_left": None,
                "view_rect_right": None,
                "source_rect_left": None,
                "source_rect_right": None,
            },
            {
                "y": 256,
                "scroll_x": 0,
                "scroll_step": 1,
                "view_rect_left": None,
                "view_rect_right": None,
                "source_rect_left": None,
                "source_rect_right": None,
            }
        ]

    def update(self, time: int):
        for layer in self.layers:
            layer['scroll_x'] += layer['scroll_step']
            if layer['scroll_x'] > self.WIDTH:
                layer['scroll_x'] = 0
            layer['view_rect_left'] = Rect(0, 0, self.WIDTH - layer['scroll_x'], self.HEIGHT)
            layer['view_rect_right'] = Rect(self.WIDTH - layer['scroll_x'], 0, layer['scroll_x'], self.HEIGHT)
            layer['source_rect_left'] = Rect(layer['scroll_x'], layer['y'], layer['view_rect_left'].w, self.HEIGHT)
            layer['source_rect_right'] = Rect(0, layer['y'], layer['view_rect_right'].w, self.HEIGHT)

    def draw(self, renderer: Renderer) -> None:
        for layer in self.layers:
            renderer.draw(SpriteRegistry.BACKGROUND, layer['source_rect_left'], layer['view_rect_left'])
            renderer.draw(SpriteRegistry.BACKGROUND, layer['source_rect_right'], layer['view_rect_right'])


class PowerUp(Sprite):
    WIDTH = 24
    HEIGHT = 19

    def __init__(self):
        super().__init__()
        self.alive = True
        self.rect = Rect(0, 0, self.WIDTH, self.HEIGHT)
        variants: list = []
        variants.append(Rect(0, 0, self.WIDTH, self.HEIGHT))  # Build power
        variants.append(Rect(24, 0, self.WIDTH, self.HEIGHT))  # Extra bullet
        variants.append(Rect(48, 0, self.WIDTH, self.HEIGHT))  # Rockets
        variants.append(Rect(72, 0, self.WIDTH, self.HEIGHT))  # Shield
        variants.append(Rect(96, 0, self.WIDTH, self.HEIGHT))  # Extra speed
        skin = randint(0, 4)
        self.src = variants[skin]
        self.vY = -10

    def update(self, time: int) -> None:
        self.rect.left -= 1
        if self.vY < 0:
            self.rect.top -= 1
            self.vY += 1
            if self.vY == 0:
                self.vY = 10
        elif self.vY > 0:
            self.rect.top += 1
            self.vY -= 1
            if self.vY == 0:
                self.vY = -10

    def draw(self, renderer: Renderer) -> None:
        renderer.draw(SpriteRegistry.POWERUP, self.src, self.rect)

    def is_alive(self) -> bool:
        return self.alive

    def destroy(self) -> None:
        self.alive = False

    def collide(self, other: Sprite) -> bool:
        if self.is_alive() is False:
            return False
        return self.rect.colliderect(other.rect)


class Explosion(Sprite):
    def __init__(self):
        super().__init__()
        self.alive = True
        self.rect = Rect(0, 0, 32, 32)
        self.frame: Frame = None
        ''' Create frames '''
        self.frames: list = []
        for i in range(17):
            if i < 10:
                self.frames.append(
                    Frame(
                        self.rect,
                        Rect(32 * i, 0, 32, 32),
                        1
                    )
                )
            else:
                self.frames.append(
                    Frame(
                        self.rect,
                        Rect(32 * (i - 10), 32, 32, 32),
                        1
                    )
                )
        ''' Setup actions '''
        action_frames: list = []
        action_frames.append(self.frames[1])
        action_frames.append(self.frames[2])
        action_frames.append(self.frames[3])
        action_frames.append(self.frames[4])
        action_frames.append(self.frames[5])
        action_frames.append(self.frames[6])
        action_frames.append(self.frames[7])
        action_frames.append(self.frames[8])
        action_frames.append(self.frames[9])
        action_frames.append(self.frames[0])
        action_frames.append(self.frames[11])
        action_frames.append(self.frames[12])
        action_frames.append(self.frames[13])
        action_frames.append(self.frames[14])
        action_frames.append(self.frames[15])
        action_frames.append(self.frames[16])
        self.action = Action(action_frames)
        self.frame = action_frames[0]

    def update(self, time: int):
        self.frame = self.action.next_frame()
        self.frame.collision.center = self.rect.center

    def draw(self, renderer: Renderer) -> None:
        renderer.draw(SpriteRegistry.EXPLOSION, self.frame.src, self.rect)

    def is_alive(self) -> bool:
        return self.alive

    def destroy(self) -> None:
        self.alive = False

    def collide(self, other: Sprite) -> bool:
        return False


class Bullet(GameObject):
    WIDTH = 11
    HEIGHT = 6

    def __init__(self):
        super().__init__()
        self.alive: bool = True
        self.speed: int = 8
        self.frame: Frame = None
        self.frames: list = []
        self.init_frames()
        self.action: Action = Action(self.frames)
        self.rect: Rect = self.frames[0].collision
        self.frame = self.frames[0]

    def init_frames(self):
        self.frames.append(
            Frame(Rect(0, 0, 11, 6), Rect(0, 5, 11, 6), 1)
        )
        self.frames.append(
            Frame(Rect(0, 0, 11, 8), Rect(16, 4, 11, 8), 1)
        )
        self.frames.append(
            Frame(Rect(0, 0, 11, 10), Rect(32, 3, 11, 10), 1)
        )
        self.frames.append(
            Frame(Rect(0, 0, 11, 12), Rect(48, 2, 11, 12), 1)
        )
        self.frames.append(
            Frame(Rect(0, 0, 11, 14), Rect(64, 1, 11, 14), 1)
        )
        self.frames.append(
            Frame(Rect(0, 0, 11, 16), Rect(80, 0, 11, 16), 1)
        )

    def update(self, time: int) -> None:
        self.rect.left += self.speed
        self.frame = self.action.next_frame()
        self.frame.collision.topleft = self.rect.topleft
        index = self.frames.index(self.frame)
        self.frame.collision.top -= index

    def draw(self, renderer: Renderer) -> None:
        renderer.draw(SpriteRegistry.BULLET, self.frame.src, self.frame.collision)

    def is_alive(self) -> bool:
        return self.alive

    def destroy(self) -> None:
        self.alive = False

    def collide(self, other: GameObject) -> bool:
        if self.is_alive() is False:
            return False
        return self.rect.colliderect(other.rect)

    def align(self, src: Rect) -> None:
        self.rect.midleft = src.center


class DiagUpBullet(Bullet):
    def __init__(self):
        super().__init__()

    def init_frames(self):
        self.frames.append(
            Frame(Rect(0, 0, 10, 10), Rect(275, 35, 10, 10), 1)
        )
        self.frames.append(
            Frame(Rect(0, 0, 15, 14), Rect(289, 33, 15, 14), 1)
        )

    def update(self, time: int) -> None:
        self.rect.left += self.speed
        self.rect.top -= self.speed
        self.frame = self.action.next_frame()
        self.frame.collision.topleft = self.rect.topleft


class DiagDownBullet(Bullet):
    def __init__(self):
        super().__init__()

    def init_frames(self):
        self.frames.append(
            Frame(Rect(0, 0, 10, 10), Rect(275, 51, 10, 10), 1)
        )
        self.frames.append(
            Frame(Rect(0, 0, 15, 14), Rect(289, 49, 15, 14), 1)
        )

    def update(self, time: int) -> None:
        self.rect.left += self.speed
        self.rect.top += self.speed
        self.frame = self.action.next_frame()
        self.frame.collision.topleft = self.rect.topleft


class Craft(GameObject):
    WIDTH = 32
    HEIGHT = 24

    def __init__(self, boundary: tuple):
        super().__init__()
        self.explosion: Explosion = Explosion()
        self.boundary = boundary
        self.speed: int = 4
        self.action: int = 0
        self.alive: bool = True
        self.rect: Rect = Rect(0, 0, self.WIDTH, 14)
        self.bullets: list = []
        self.shoot_tick: int = 0
        self.frame: Frame = None
        ''' Setup frames '''
        self.frames: list = []
        self.actions: list = []
        off_x = 0
        off_y = 0
        for i in range(14):
            if i == 5 or i == 10:
                off_x = 0
                off_y += 1
            self.frames.append(
                Frame(
                    Rect(0, 0, self.WIDTH, 14),
                    Rect(off_x * self.WIDTH, off_y * self.HEIGHT, self.WIDTH, self.HEIGHT),
                    1
                )
            )
            off_x += 1
        ''' Setup actions '''
        self.actions.append(Action([self.frames[0]]))  # Flying
        self.actions.append(Action([self.frames[1], self.frames[2]]))  # Up
        self.actions.append(Action([self.frames[3], self.frames[4]]))  # Down
        self.actions.append(Action([self.frames[2], self.frames[1], self.frames[0]]))  # Restore Up
        self.actions.append(Action([self.frames[4], self.frames[3], self.frames[0]]))  # Restore Down

    def set_input(self, input: Input) -> None:
        self.input = input

    def update(self, time: int) -> None:
        if self.is_alive() is False:
            self.explosion.update(time)
            self.update_bullets(time)
            return
        ''' Update velocity according to user input '''
        vel = Vector2(0, 0)
        dir = self.input.get_direction()
        vel.x = dir.x * self.speed
        vel.y = dir.y * self.speed
        ''' define current action '''
        if dir.y < 0:
            self.action = 1  # Move up
        if dir.y > 0:
            self.action = 2  # Move down
        if dir.y == 0:  # Restore animation from up or down motion.
            if self.action == 1 or self.action == 3:
                self.action = 3
            elif self.action == 2 or self.action == 4:
                self.action = 4
            else:
                self.action = 0
        ''' end define current action '''
        self.frame = self.actions[self.action].next_frame()

        ''' When action is change then reset the state of other actions '''
        for i, action in enumerate(self.actions):
            if i != self.action:
                action.reset()

        ''' Store the current position to the sprite rect '''
        self.rect.left += vel.x
        self.rect.top += vel.y

        ''' Update the sprite rect after checking any collision with screen boundaries. '''
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.left > self.boundary[0] - self.WIDTH:
            self.rect.left = self.boundary[0] - self.WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.top > self.boundary[1] - self.HEIGHT:
            self.rect.top = self.boundary[1] - self.HEIGHT

        ''' Update the position of the frame according to current sprite rect '''
        self.frame.collision.topleft = self.rect.topleft
        buttons = self.input.get_buttons()
        if buttons.is_pressed(State.X):
            self.shoot(time)
        self.update_bullets(time)

    def update_bullets(self, time: int):
        for bullet in self.bullets:
            bullet.update(time)
            if bullet.rect.left > self.boundary[0] or bullet.rect.bottom < 0 \
                    or bullet.rect.top > self.boundary[1] or bullet.is_alive() is False:
                self.bullets.remove(bullet)

    def shoot(self, time: int) -> None:
        ''' Add delay for each bullet shooting '''
        if self.shoot_tick < 5 and len(self.bullets) > 0:
            self.shoot_tick += 1
            return
        self.shoot_tick = 0
        blts = [Bullet(), DiagUpBullet(), DiagDownBullet()]
        for tmp in blts:
            self.bullets.append(tmp)
            tmp.align(self.rect)
        post(Event(Engine.GAME_EVENT, gtype=Engine.CRAFT_SHOOTED))

    def draw(self, renderer: Renderer) -> None:
        if self.is_alive() is False:
            self.explosion.draw(renderer)
            self.draw_bullets(renderer)
            return
        renderer.draw(SpriteRegistry.CRAFT, self.frame.src, self.frame.collision)
        self.draw_bullets(renderer)

    def draw_bullets(self, renderer: Renderer):
        for bullet in self.bullets:
            bullet.draw(renderer)

    def is_alive(self) -> bool:
        return self.alive

    def destroy(self) -> None:
        self.alive = False
        self.explosion.rect.center = self.rect.center

    def collide(self, other: GameObject) -> bool:
        for b in self.bullets:
            if other.is_alive() and b.collide(other):
                b.destroy()
                return True
        return False

    def killed(self, other: GameObject):
        pass

    def spawn(self) -> None:
        self.alive = True


class Asteroid(GameObject):
    def __init__(self, boundary: tuple):
        super().__init__()
        self.alive = True
        self.life = 2
        self.explosion = Explosion()
        self.speed = randint(3, 5)
        self.bonus = self.speed
        self.variants: list = []
        self.variants.append(Rect(145, 130, 30, 36))
        self.variants.append(Rect(146, 170, 30, 29))
        self.variants.append(Rect(193, 228, 47, 51))
        self.variants.append(Rect(240, 225, 48, 53))
        self.variants.append(Rect(147, 288, 61, 72))
        self.variants.append(Rect(208, 282, 109, 77))
        skin = randint(0, 4)
        if skin > 1 and skin < 4:
            self.life = 4
        elif skin >= 4:
            self.life = 6
        self.src_rect = self.variants[skin]
        self.rect = Rect(
            boundary[0],
            randint(0, boundary[1] - self.src_rect.height),
            self.src_rect.width,
            self.src_rect.height)

    def update(self, time: int) -> None:
        if self.is_alive() is False:
            self.explosion.update(time)
            return
        self.rect.left -= self.speed

    def draw(self, renderer: Renderer) -> None:
        if self.is_alive() is False:
            self.explosion.draw(renderer)
            return
        renderer.draw(SpriteRegistry.ASTEROID, self.src_rect, self.rect)

    def is_alive(self) -> bool:
        return self.alive

    def destroy(self) -> None:
        self.life -= 1
        if self.life <= 0:
            self.alive = False
            self.explosion.rect.center = self.rect.center
            post(Event(Engine.GAME_EVENT, gtype=Engine.ENEMY_DESTROYED, bonus=self.bonus))

    def collide(self, other: GameObject) -> bool:
        if self.is_alive() is False:
            return False
        return self.rect.colliderect(other.rect)

    def powerup(self) -> Optional[PowerUp]:
        pass


class AsteroidWave(GameObject):

    def __init__(self, boundary: tuple):
        super().__init__()
        self.items: list = []
        self.timer = Timer(300)
        self.boundary: tuple = boundary

    def update(self, time: int) -> None:
        if self.timer.looped(time):
            self.items.append(Asteroid(self.boundary))
        for item in self.items:
            item.update(time)
            if item.rect.right < 0:
                self.items.remove(item)

    def draw(self, renderer: Renderer) -> None:
        for item in self.items:
            item.draw(renderer)

    def collide(self, other: Craft) -> list:
        hits: list = []
        for item in self.items:
            if other.collide(item):
                item.destroy()
                if item.is_alive() is False:
                    hits.append(item)
                    self.items.remove(item)
            if item.collide(other):
                other.destroy()
        return hits


class FontSprite(Sprite):
    WIDTH = 12
    HEIGHT = 12
    CHAR_PER_ROW = 29

    def __init__(self):
        super().__init__()
        self.letters: list = []
        self.chars = ['!', '"', '#', '$', '%', '&', '\'', '(', ')', '*', '+',
                      ',', '-', '.', '/', '0', '1', '2', '3', '4', '5', '6',
                      '7', '8', '9', ':', ';', '<', '=', '>', '?', '@', 'A',
                      'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
                      'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W',
                      'X', 'Y', 'Z', '[', '\\', ']', '^', '_', '`', 'a', 'b',
                      'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']

    def display(self, text: str) -> None:
        self.letters = [char for char in text]

    def draw(self, renderer: Renderer) -> None:
        cursor: int = 120
        for char in self.letters:
            n = self.chars.index(char)
            y = (n // self.CHAR_PER_ROW) * self.HEIGHT
            x = (n % (self.CHAR_PER_ROW + 1)) * self.WIDTH
            src = Rect(x, y, self.WIDTH, self.HEIGHT)
            dest = Rect(cursor, 10, self.WIDTH, self.HEIGHT)
            renderer.draw(SpriteRegistry.FONTS, src, dest)
            cursor += 8
