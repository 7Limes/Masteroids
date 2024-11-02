from pygame import Vector2
import util
from globals import resource_manager


RADIUS = 3.0
FRAME_DURATION = 0.25

class LevelEnd(util.AnimatedLevelObject):
    def __init__(self, position: Vector2):
        level_end_sheet = resource_manager.get_full_spritesheet('level_end_ss')
        super().__init__(position, RADIUS, Vector2(0, 0), level_end_sheet, FRAME_DURATION)