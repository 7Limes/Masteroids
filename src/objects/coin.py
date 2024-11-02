from pygame import Vector2, Surface
import util
from globals import resource_manager
from resource_manager import AnimationManager


RADIUS = 0.75
ANIMATION_FRAME_DURATION = 0.5


class Coin(util.AnimatedLevelObject):
    def __init__(self, position: Vector2):
        coin_sprites = resource_manager.get_full_spritesheet('coin')
        super().__init__(position, RADIUS, Vector2(0, 0), coin_sprites, ANIMATION_FRAME_DURATION)