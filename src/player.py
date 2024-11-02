import pygame
from pygame import Vector2, Surface

from resource_manager import ResourceManager
import util


ROTATE_SPEED = 100
THRUST_STRENGTH = 1
MAX_SPEED = 10

class Player:
    def __init__(self):
        self.position = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        self.angle: float = 0.0

    
    def handle_input(self, delta: float, keys: pygame.key.ScancodeWrapper):
        if keys[pygame.K_LEFT]:
            self.angle += ROTATE_SPEED * delta
        if keys[pygame.K_RIGHT]:
            self.angle -= ROTATE_SPEED * delta
        self.angle = util.wrap(self.angle, 0, 360)
        
        if keys[pygame.K_UP]:
            thrust_vector: Vector2 = Vector2.from_polar((1, self.angle)) * THRUST_STRENGTH
            thrust_vector.y *= -1
            self.velocity += thrust_vector * delta
            self.velocity.clamp_magnitude_ip(MAX_SPEED)
    

    def update(self, delta: float):
        self.position += self.velocity * delta
    

    def draw(self, surf: Surface, resource_manager: ResourceManager):
        surf_center = Vector2(surf.get_size()) / 2
        player_sprite = resource_manager.get_image('player')
        player_sprite_rotated = pygame.transform.rotate(player_sprite, self.angle)
        half_sprite_size = Vector2(player_sprite_rotated.get_size()) / 2
        surf.blit(player_sprite_rotated, surf_center-half_sprite_size)