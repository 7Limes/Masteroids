from pygame import Vector2, Surface
import util
from util import CollisionCircle


class Asteroid(CollisionCircle):
    def __init__(self, position: Vector2, radius: float):
        super().__init__(position, radius)
    

    def draw(self, surf: Surface, view_pos: Vector2):
        screen_coord = util.world_to_screen(surf, view_pos, self.position, util.RENDER_SCALE)
        super().draw(surf, screen_coord)