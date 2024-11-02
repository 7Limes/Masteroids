from pygame import Vector2, Surface
import util
from util import DynamicCollisionCircle


class Asteroid(DynamicCollisionCircle):
    def __init__(self, position: Vector2, radius: float, velocity: Vector2):
        super().__init__(position, radius, velocity)
    

    def draw(self, surf: Surface, view_pos: Vector2):
        screen_coord = util.world_to_screen(surf, view_pos, self.position, util.RENDER_SCALE)
        super().draw(surf, screen_coord)