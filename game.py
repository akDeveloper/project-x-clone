from engine import GameState
from renderer import Renderer
from sprites import Background, Craft, Bullet, Asteroid, Explosion
from controls import Input
from pygame import Rect


class LoadState(GameState):
    LEVEL_1_SPRITES = 3

    def __init__(self, renderer: Renderer):
        self.renderer: Renderer = renderer
        self.renderer.register_image(Background.REGISTRY, "assets/background.png")
        self.renderer.register_image(Craft.REGISTRY, "assets/pxplayer.png")
        self.renderer.register_image(Bullet.REGISTRY, "assets/bullets.png")
        self.renderer.register_image(self.LEVEL_1_SPRITES, "assets/level1_sprites.png")
        self.renderer.register_image(Explosion.REGISTRY, "assets/explosion.png")
        self.background: Background = Background()
        self.craft: Craft = Craft(renderer.bb_size)

    def update(self, time: int, input: Input) -> None:
        pass

    def draw(self, renderer: Renderer) -> None:
        pass

    def state(self) -> GameState:
        return GetReadyState(self)


class GetReadyState(GameState):
    def __init__(self, state: GameState):
        self.ticks = 0
        self.renderer: Renderer = state.renderer
        self.background: Background = state.background
        self.craft: Craft = Craft(self.renderer.bb_size)

    def update(self, time: int, input: Input) -> None:
        self.background.update(time)
        self.craft.set_input(input)
        self.craft.update(time)
        self.ticks += 1

    def draw(self, renderer: Renderer) -> None:
        self.background.draw(renderer)
        self.craft.draw(renderer)
        self.renderer.draw(Bullet.REGISTRY, Rect(0, 64, 144, 32), Rect(100, 100, 144, 32))

    def state(self) -> GameState:
        if self.ticks < 100:
            return self
        return PlayState(self)


class PlayState(GameState):
    def __init__(self, state: GetReadyState):
        self.renderer: Renderer = state.renderer
        self.background: Background = state.background
        self.craft: Craft = state.craft
        self.asteroids: list = []
        self.__asteroids_tick: int = 0
        self.__dead_tick: int = 0

    def update(self, time: int, input: Input) -> None:
        self.background.update(time)
        self.craft.set_input(input)
        self.craft.update(time)
        self.generate_asteroids()
        self.update_asteroids(time)
        self.check_collision()

    def draw(self, renderer: Renderer) -> None:
        self.background.draw(renderer)
        self.draw_asteroids(renderer)
        self.craft.draw(renderer)

    def state(self) -> GameState:
        if self.craft.is_alive() is False:
            if self.__dead_tick > 100:
                return GetReadyState(self)
            self.__dead_tick += 1
        return self

    def generate_asteroids(self) -> None:
        if self.__asteroids_tick < 50:
            self.__asteroids_tick += 1
            return
        self.asteroids.append(Asteroid(self.renderer.bb_size))
        self.__asteroids_tick = 0

    def update_asteroids(self, time) -> None:
        for a in self.asteroids:
            a.update(time)
            if a.rect.right < 0:
                self.asteroids.remove(a)

    def draw_asteroids(self, renderer: Renderer):
        for a in self.asteroids:
            a.draw(renderer)

    def check_collision(self) -> None:
        for a in self.asteroids:
            if self.craft.collide(a):
                a.destroy()
            if a.collide(self.craft):
                self.craft.destroy()
