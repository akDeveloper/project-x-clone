from engine import GameState
from renderer import Renderer
from sprites import Background, Craft, Bullet
from controls import Input


class PlayState(GameState):
    def __init__(self, renderer: Renderer):
        self.__renderer: Renderer = renderer
        self.__background = Background()
        self.__renderer.register_image(Background.REGISTRY, "assets/background.png")
        self.__craft = Craft(renderer.bb_size)
        self.__renderer.register_image(Craft.REGISTRY, "assets/pxplayer.png")
        self.__renderer.register_image(Bullet.REGISTRY, "assets/bullets.png")

    def update(self, time: int, input: Input) -> None:
        self.__background.update(time)
        self.__craft.set_input(input)
        self.__craft.update(time)

    def draw(self, renderer: Renderer) -> None:
        self.__background.draw(renderer)
        self.__craft.draw(renderer)

    def state(self) -> GameState:
        return self
