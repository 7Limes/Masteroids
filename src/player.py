from pygame import Vector2, Surface

from resource_manager import ResourceManager

class Player:
    def __init__(self):
        self.position = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
    

    def draw(self, surf: Surface, resource_manager: ResourceManager):
        surf_center = Vector2(surf.get_size()) / 2
        player_sprite = resource_manager.get_image('player')
        half_sprite_size = Vector2(player_sprite.get_size()) / 2
        surf.blit(player_sprite, surf_center-half_sprite_size)