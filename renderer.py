from pygame import Surface, Rect, image, init, HWSURFACE, DOUBLEBUF, FULLSCREEN
from pygame.transform import scale
from pygame.display import set_mode, update
from enum import Enum


class SpriteRegistry(Enum):
    BACKGROUND = 0
    CRAFT = 1
    BULLET = 2
    ASTEROID = 3
    EXPLOSION = 4
    FONTS = 5
    POWERUP = 6


class Renderer(object):
    def __init__(self, bb_width: int, bb_height: int, sc_width: int, sc_height: int, fullscreen: bool = False):
        pass

    def draw_to_screen(self) -> None:
        pass

    def cls(self) -> None:
        pass

    def register_image(self, name: int, filepath: str) -> None:
        pass

    def draw(self, name: int, src: Rect, dest: Rect) -> None:
        pass


class SdlRenderer(Renderer):
    def __init__(self, bb_width: int, bb_height: int, sc_width: int, sc_height: int, fullscreen: bool = False):
        init()
        self.bb_size = (bb_width, bb_height)
        self.__images: list = []
        self.__size = (sc_width, sc_height)
        if fullscreen is True:
            self.__screen = set_mode(self.__size, HWSURFACE | DOUBLEBUF | FULLSCREEN)
        else:
            self.__screen = set_mode(self.__size)
        """ backbuffer Surface for handling the small graphics """
        self.__backbuffer = Surface(self.bb_size)

    def draw_to_screen(self) -> None:
        self.__backbuffer.convert_alpha()
        """ upscale backbuffer to screen """
        scale(self.__backbuffer, self.__size, self.__screen)
        update()

    def cls(self) -> None:
        self.__backbuffer.fill((21, 21, 21))

    def register_image(self, spr: SpriteRegistry, filepath: str) -> None:
        self.__images.insert(spr.value, image.load(filepath).convert_alpha())

    def draw(self, spr: SpriteRegistry, src: Rect, dest: Rect, flags: int = 0) -> None:
        self.__backbuffer.blit(self.__images[spr.value], dest, src, flags)
