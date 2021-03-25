from pygame import Rect


class Frame(object):
    def __init__(self, col: Rect, src: Rect, delay: int):
        self.collision: Rect = col
        self.src: Rect = src
        self.delay = delay


class Action(object):
    def __init__(self, frames: list):
        self.tick: int = 0
        self.index: int = 0
        self.frames: list = frames

    def next_frame(self) -> int:
        frame: Frame = self.frames[self.index]
        if self.tick > frame.delay:
            self.tick = 0
            self.index += 1
            if self.index >= len(self.frames):
                self.index = len(self.frames) - 1
        self.tick += 1
        return frame

    def reset(self) -> None:
        self.tick = 0
        self.index = 0
