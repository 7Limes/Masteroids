from resource_manager import ResourceManager
from particle.particle import ParticleEffect


resource_manager: ResourceManager = ResourceManager()
particle_effects: list[ParticleEffect] = []


def load_resources():
    global resource_manager
    resource_manager.load_image('player', 'assets/temp-player.png')
    resource_manager.load_image('asteroid', 'assets/temp-asteroid.png')
    resource_manager.load_image('dest_asteroid', 'assets/temp-dest-asteroid.png')
    resource_manager.load_image('spark', 'assets/spark.png')