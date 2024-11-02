from pygame import Vector2
import util
from globals import resource_manager


RADIUS = 2.0

class LevelEnd(util.LevelObject):
    def __init__(self, position: util.Vector2):
        level_end_sprite = resource_manager.load_image('level_end')
        super().__init__(position, RADIUS, Vector2(0, 0), level_end_sprite)