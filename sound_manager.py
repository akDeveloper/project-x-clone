import pygame.mixer as mixer


class SoundManager(object):
    FIRE = 1
    EXPLODE = 2
    PLAYER_EXPLODE = 3

    def __init__(self):
        self.sounds = {
            self.FIRE: mixer.Sound('assets/sounds/Retro_8-Bit_Game-Gun_Laser_Weapon_Shoot_Beam_07.wav'),
            self.EXPLODE: mixer.Sound('assets/sounds/Retro_8-Bit_Game-Bomb_Explosion_08.wav'),
            self.PLAYER_EXPLODE: mixer.Sound('assets/sounds/Retro_8-Bit_Game-Bomb_Explosion_02.wav'),
        }
        self.sounds.get(self.FIRE).set_volume(0.5)
        self.music = mixer.Sound('assets/sounds/space-asteroids.ogg')

    def play(self, type: int) -> None:
        mixer.Channel(type).play(self.sounds.get(type))

    def start_music(self, loop: int = -1) -> None:
        self.music.play(loop)
