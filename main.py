from engine import Engine
from renderer import SdlRenderer
from game import PlayState


def main():
    renderer = SdlRenderer(320, 256, 640, 512)
    engine: Engine = Engine(renderer)
    engine.run(PlayState(renderer))


if __name__ == "__main__":
    main()
