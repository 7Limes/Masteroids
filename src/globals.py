from enum import Enum
from pathlib import Path
import sys
import os
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
keyboard_aim = False


def get_assets_path() -> str:
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = str(Path(__file__).resolve().parent.parent)
    
    return os.path.join(base_path, 'assets')


ASSETS_PATH = get_assets_path()


def set_game_state(state: GameState):
    global game_state
    game_state = state


def load_resources():
    global resource_manager
    resource_manager.load_image('player', f'{ASSETS_PATH}/player.png')
    resource_manager.load_image('asteroid', f'{ASSETS_PATH}/asteroid.png')
    resource_manager.load_image('coin_asteroid', f'{ASSETS_PATH}/coin_asteroid.png')
    resource_manager.load_image('orbiter', f'{ASSETS_PATH}/orbiter.png')
    resource_manager.load_image('smart_orbiter', f'{ASSETS_PATH}/smart_orbiter.png')
    resource_manager.load_image('long_orbiter', f'{ASSETS_PATH}/long_orbiter.png')

    resource_manager.load_image('fire_rate_icon', f'{ASSETS_PATH}/shoot_upgrade.png')
    resource_manager.load_image('brakes_icon', f'{ASSETS_PATH}/brakes_upgrade.png')
    resource_manager.load_image('thrust_icon', f'{ASSETS_PATH}/fire_upgrade.png')

    resource_manager.load_image('space_bg', f'{ASSETS_PATH}/space_bg.png')
    resource_manager.load_image('menu_bg', f'{ASSETS_PATH}/menu_bg.png')

    resource_manager.load_spritesheet('fragments', f'{ASSETS_PATH}/fragments.png', [8, 8])
    resource_manager.load_spritesheet('coin', f'{ASSETS_PATH}/coin.png', [8, 8])
    resource_manager.load_spritesheet('level_end_ss', f'{ASSETS_PATH}/level_end_ss.png', [25, 25])
    resource_manager.load_spritesheet('explosion', f'{ASSETS_PATH}/explosion.png', [200, 250])

    resource_manager.load_sound('shoot', f'{ASSETS_PATH}/audio/shoot.wav')
    resource_manager.load_sound('hit', f'{ASSETS_PATH}/audio/hit.wav')
    resource_manager.load_sound('explosion', f'{ASSETS_PATH}/audio/explosion.wav')
    resource_manager.load_sound('coin', f'{ASSETS_PATH}/audio/coin.wav')
    resource_manager.load_sound('hook', f'{ASSETS_PATH}/audio/hook.wav')
    resource_manager.load_sound('blip', f'{ASSETS_PATH}/audio/blip.wav')
    resource_manager.load_sound('death', f'{ASSETS_PATH}/audio/death.wav')
    resource_manager.load_sound('deltarune_explosion', f'{ASSETS_PATH}/audio/deltarune_explosion.mp3')
    resource_manager.load_sound('upgrade', f'{ASSETS_PATH}/audio/upgrade.wav')
    resource_manager.load_sound('end_level', f'{ASSETS_PATH}/audio/end_level.wav')