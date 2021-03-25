from pygame.sprite import Sprite
from pygame import Rect
from renderer import Renderer
from action import Frame, Action
from controls import Input, State
from pygame.math import Vector2


class Background(Sprite):
    REGISTRY = 0
    WIDTH = 512
    HEIGHT = 256

    def __init__(self):
        super().__init__()
        self.input: Input = None
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
                "scroll_step": 0.3,
                "view_rect_left": None,
                "view_rect_right": None,
                "source_rect_left": None,
                "source_rect_right": None,
            },
            {
                "y": 1792,
                "scroll_x": 0,
                "scroll_step": 0.3,
                "view_rect_left": None,
                "view_rect_right": None,
                "source_rect_left": None,
                "source_rect_right": None,
            },
            {
                "y": 1536,
                "scroll_x": 0,
                "scroll_step": 0.3,
                "view_rect_left": None,
                "view_rect_right": None,
                "source_rect_left": None,
                "source_rect_right": None,
            },
            {
                "y": 1024,
                "scroll_x": 0,
                "scroll_step": 0.5,
                "view_rect_left": None,
                "view_rect_right": None,
                "source_rect_left": None,
                "source_rect_right": None,
            },
            {
                "y": 1280,
                "scroll_x": 0,
                "scroll_step": 0.5,
                "view_rect_left": None,
                "view_rect_right": None,
                "source_rect_left": None,
                "source_rect_right": None,
            },
            {
                "y": 512,
                "scroll_x": 0,
                "scroll_step": 0.5,
                "view_rect_left": None,
                "view_rect_right": None,
                "source_rect_left": None,
                "source_rect_right": None,
            },
            {
                "y": 256,
                "scroll_x": 0,
                "scroll_step": 0.5,
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
            renderer.draw(self.REGISTRY, layer['source_rect_left'], layer['view_rect_left'])
            renderer.draw(self.REGISTRY, layer['source_rect_right'], layer['view_rect_right'])

    def registry(self):
        return self.REGISTRY


class Explosion(Sprite):
    def __init__(self):
        super().__init__()


class Bullet(Sprite):
    REGISTRY = 2
    WIDTH = 11
    HEIGHT = 6

    def __init__(self):
        super().__init__()
        self.alive: bool = True
        self.speed: int = 3
        self.rect: Rect = Rect(0, 0, self.WIDTH, self.HEIGHT)
        self.src_rect: Rect = Rect(0, 5, self.WIDTH, self.HEIGHT)

    def update(self, time: int) -> None:
        self.rect.left += self.speed

    def draw(self, renderer: Renderer) -> None:
        renderer.draw(self.REGISTRY, self.src_rect, self.rect)

    def is_alive(self) -> bool:
        return self.alive

    def destroy(self) -> None:
        self.alive = False


class Craft(Sprite):
    REGISTRY = 1
    WIDTH = 32
    HEIGHT = 24

    def __init__(self, boundary: tuple):
        super().__init__()
        self.boundary = boundary
        self.speed: int = 2
        self.action: int = 0
        self.alive: bool = True
        self.rect: Rect = Rect(0, 0, self.WIDTH, 14)
        self.bullets: list = []
        self.bullet_tick: int = 0
        self.frame: Frame = None
        ''' Create frames '''
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
                    3
                )
            )
            off_x += 1
        self.actions.append(Action([self.frames[0]]))  # Flying
        self.actions.append(Action([self.frames[1], self.frames[2]]))  # Up
        self.actions.append(Action([self.frames[3], self.frames[4]]))  # Down
        self.actions.append(Action([self.frames[2], self.frames[1], self.frames[0]]))  # Restore Up
        self.actions.append(Action([self.frames[4], self.frames[3], self.frames[0]]))  # Restore Down

    def set_input(self, input: Input) -> None:
        self.input = input

    def update(self, time: int) -> None:
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
        for bullet in self.bullets:
            bullet.update(time)
            if bullet.rect.left > self.boundary[0] or bullet.is_alive() is False:
                self.bullets.remove(bullet)

    def shoot(self, time: int) -> None:
        if self.bullet_tick < 20 and len(self.bullets) > 0:
            self.bullet_tick += 1
            return
        self.bullet_tick = 0
        tmp = Bullet()
        self.bullets.append(tmp)
        tmp.rect.move_ip(self.rect.left + 22, self.rect.top + 12)

    def draw(self, renderer: Renderer) -> None:
        renderer.draw(self.REGISTRY, self.frame.src, self.frame.collision)
        for bullet in self.bullets:
            bullet.draw(renderer)

    def registry(self) -> int:
        return self.REGISTRY

    def is_alive(self) -> bool:
        return self.alive

    def destroy(self) -> None:
        self.alive = False
