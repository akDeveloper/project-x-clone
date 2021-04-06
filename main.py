from engine import Engine
from renderer import SdlRenderer
from game import LoadState


def main():
    renderer = SdlRenderer(320, 240, 800, 600)
    engine: Engine = Engine(renderer)
    engine.run(LoadState(renderer))


if __name__ == "__main__":
    main()
