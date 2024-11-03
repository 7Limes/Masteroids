from enum import Enum
from resource_manager import ResourceManager
from particle.particle import ParticleEffect
from util import CollisionCircle
from ui.ui import UiHandler


class GameStateEnum(Enum):
    MENU = 0
    PAUSE = 1
    LEVEL = 2
    UPGRADE = 3
    GAME_OVER = 4


class GameState:
    def __init__(self, state: GameStateEnum):
        self.state = state
    
    def set_state(self, state: GameStateEnum):
        self.state = state


resource_manager: ResourceManager = ResourceManager()
particle_effects: list[ParticleEffect] = []
added_level_objects: list[CollisionCircle] = []
game_state = GameState(GameStateEnum.LEVEL)
ui_handler: UiHandler = UiHandler([])


def set_game_state(state: GameState):
    global game_state
    game_state = state


def load_resources():
    global resource_manager
    resource_manager.load_image('player', 'assets/temp-player.png')
    resource_manager.load_image('asteroid', 'assets/temp-asteroid.png')
    resource_manager.load_image('dest_asteroid', 'assets/temp-dest-asteroid.png')
    resource_manager.load_image('upgrade', 'assets/upgrade.png')
    resource_manager.load_image('orbiter', 'assets/orbiter.png')

    resource_manager.load_image('space_bg', 'assets/space_bg.png')
    resource_manager.load_image('menu_bg', 'assets/menu_bg.png')

    resource_manager.load_spritesheet('fragments', 'assets/fragments.png', [8, 8])
    resource_manager.load_spritesheet('coin', 'assets/coin.png', [8, 8])
    resource_manager.load_spritesheet('level_end_ss', 'assets/level_end_ss.png', [25, 25])
    resource_manager.load_spritesheet('explosion', 'assets/explosion.png', [200, 250])

    resource_manager.load_sound('shoot', 'assets/audio/shoot.wav')
    resource_manager.load_sound('hit', 'assets/audio/hit.wav')
    resource_manager.load_sound('explosion', 'assets/audio/explosion.wav')
    resource_manager.load_sound('coin', 'assets/audio/coin.wav')
    resource_manager.load_sound('hook', 'assets/audio/hook.wav')
    resource_manager.load_sound('thrust', 'assets/audio/thrust.wav')
    resource_manager.load_sound('blip', 'assets/audio/blip.wav')
    resource_manager.load_sound('death', 'assets/audio/death.wav')
    resource_manager.load_sound('deltarune_explosion', 'assets/audio/deltarune_explosion.mp3')