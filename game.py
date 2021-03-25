from engine import GameState
from renderer import Renderer
from sprites import Background, Craft, Bullet, Asteroid, Explosion
from controls import Input


class PlayState(GameState):
    LEVEL_1_SPRITES = 3

    def __init__(self, renderer: Renderer):
        self.__renderer: Renderer = renderer
        self.__background: Background = Background()
        self.__renderer.register_image(Background.REGISTRY, "assets/background.png")
        self.__craft: Craft = Craft(renderer.bb_size)
        self.__renderer.register_image(Craft.REGISTRY, "assets/pxplayer.png")
        self.__renderer.register_image(Bullet.REGISTRY, "assets/bullets.png")
        self.__renderer.register_image(self.LEVEL_1_SPRITES, "assets/level1_sprites.png")
        self.__renderer.register_image(Explosion.REGISTRY, "assets/explosion.png")
        self.__asteroids: list = []
        self.__asteroids_tick: int = 0
        # self.__asteroids.append(Asteroid(renderer.bb_size))

    def update(self, time: int, input: Input) -> None:
        self.__background.update(time)
        self.__craft.set_input(input)
        self.__craft.update(time)
        self.generate_asteroids()
        self.update_asteroids(time)
        self.check_collision()

    def draw(self, renderer: Renderer) -> None:
        self.__background.draw(renderer)
        self.draw_asteroids(renderer)
        self.__craft.draw(renderer)

    def state(self) -> GameState:
        return self

    def generate_asteroids(self) -> None:
        if self.__asteroids_tick < 50:
            self.__asteroids_tick += 1
            return
        self.__asteroids.append(Asteroid(self.__renderer.bb_size))
        self.__asteroids_tick = 0

    def update_asteroids(self, time) -> None:
        for a in self.__asteroids:
            a.update(time)
            if a.rect.right < 0:
                self.__asteroids.remove(a)

    def draw_asteroids(self, renderer: Renderer):
        for a in self.__asteroids:
            a.draw(renderer)

    def check_collision(self) -> None:
        for a in self.__asteroids:
            if self.__craft.collide(a):
                a.destroy()
            if a.collide(self.__craft):
                self.__craft.destroy()
