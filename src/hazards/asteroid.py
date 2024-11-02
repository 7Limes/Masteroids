import pygame
from pygame import Vector2, Surface
import util
from resource_manager import ResourceManager


class Asteroid(util.DynamicCollisionCircle):
    def __init__(self, position: Vector2, radius: float, velocity: Vector2):
        super().__init__(position, radius, velocity)
    

    def draw(self, surf: Surface, view_pos: Vector2, resource_manager: ResourceManager):
        asteroid_sprite = resource_manager.get_image('asteroid')

        scaled_sprite_size = self.radius * 2 * util.RENDER_SCALE
        scaled_sprite_size_vec = Vector2(scaled_sprite_size, scaled_sprite_size)
        scaled_asteroid_sprite = pygame.transform.scale(asteroid_sprite, Vector2(scaled_sprite_size, scaled_sprite_size))

        screen_coord = util.world_to_screen(surf, view_pos, self.position, util.RENDER_SCALE)
        surf.blit(scaled_asteroid_sprite, screen_coord - scaled_sprite_size_vec / 2.0)
        super().draw(surf, screen_coord)  # draw debug hitbox