from resource_manager import ResourceManager
from particle.particle import ParticleEffect
from util import CollisionCircle


resource_manager: ResourceManager = ResourceManager()
particle_effects: list[ParticleEffect] = []
added_level_objects: list[CollisionCircle] = []


def load_resources():
    global resource_manager
    resource_manager.load_image('player', 'assets/temp-player.png')
    resource_manager.load_image('asteroid', 'assets/temp-asteroid.png')
    resource_manager.load_image('dest_asteroid', 'assets/temp-dest-asteroid.png')
    resource_manager.load_image('level_end', 'assets/level_end.png')

    resource_manager.load_spritesheet('fragments', 'assets/fragments.png')
    resource_manager.load_spritesheet('coin', 'assets/coin.png')

    resource_manager.load_sound('shoot', 'assets/audio/shoot.wav')
    resource_manager.load_sound('hit', 'assets/audio/hit.wav')
    resource_manager.load_sound('explosion', 'assets/audio/explosion.wav')
    resource_manager.load_sound('coin', 'assets/audio/coin.wav')