import pygame
from pygame import Vector2, Surface
import util
from resource_manager import ResourceManager


class Asteroid(util.DynamicCollisionCircle):
    def __init__(self, position: Vector2, radius: float, velocity: Vector2, mass: float):
        super().__init__(position, radius, velocity, mass)
    

    def draw(self, surf: Surface, view_pos: Vector2, resource_manager: ResourceManager):
        asteroid_sprite = resource_manager.get_image('asteroid')

        scaled_sprite_size = self.radius * 2 * util.RENDER_SCALE
        scaled_sprite_size_vec = Vector2(scaled_sprite_size, scaled_sprite_size)
        scaled_asteroid_sprite = pygame.transform.scale(asteroid_sprite, Vector2(scaled_sprite_size, scaled_sprite_size))

        screen_coord = self.get_screen_coord(surf, view_pos)
        surf.blit(scaled_asteroid_sprite, screen_coord - scaled_sprite_size_vec / 2.0)
        super().draw(surf, view_pos)  # draw debug hitbox