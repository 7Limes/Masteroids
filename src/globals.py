from enum import Enum
from resource_manager import ResourceManager
from particle.particle import ParticleEffect
from util import CollisionCircle


class GameState(Enum):
    MENU = 0
    PAUSE = 1
    LEVEL = 2
    UPGRADE = 3


resource_manager: ResourceManager = ResourceManager()
particle_effects: list[ParticleEffect] = []
added_level_objects: list[CollisionCircle] = []
game_state = GameState.LEVEL


def load_resources():
    global resource_manager
    resource_manager.load_image('player', 'assets/temp-player.png')
    resource_manager.load_image('asteroid', 'assets/temp-asteroid.png')
    resource_manager.load_image('dest_asteroid', 'assets/temp-dest-asteroid.png')

    resource_manager.load_image('space_bg', 'assets/space_bg.png')

    resource_manager.load_spritesheet('fragments', 'assets/fragments.png')
    resource_manager.load_spritesheet('coin', 'assets/coin.png')
    resource_manager.load_spritesheet('level_end_ss', 'assets/level_end_ss.png')

    resource_manager.load_sound('shoot', 'assets/audio/shoot.wav')
    resource_manager.load_sound('hit', 'assets/audio/hit.wav')
    resource_manager.load_sound('explosion', 'assets/audio/explosion.wav')
    resource_manager.load_sound('coin', 'assets/audio/coin.wav')
    resource_manager.load_sound('hook', 'assets/audio/hook.wav')