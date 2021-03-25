from engine import Engine
from renderer import SdlRenderer
from game import LoadState


def main():
    renderer = SdlRenderer(320, 256, 640, 512)
    engine: Engine = Engine(renderer)
    engine.run(LoadState(renderer))


if __name__ == "__main__":
    main()
