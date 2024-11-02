import pygame
from pygame import Vector2, Surface

import util
from util import DynamicCollisionCircle
from objects.asteroid import Asteroid
from globals import resource_manager, added_level_objects


ROTATE_SPEED = 180.0
THRUST_STRENGTH = 25.0
MAX_SPEED = 30.0
BRAKE_STRENGTH = 0.55
COLLISION_RADIUS = 1.25

BULLET_RADIUS = 0.2
BULLET_SPEED = 20.0
SHOOT_COOLDOWN = 0.4
BULLET_LIFETIME = 3.0


class PlayerBullet(DynamicCollisionCircle):
    def __init__(self, position: Vector2, velocity: Vector2):
        super().__init__(position, BULLET_RADIUS, velocity)
        self.lifetime = BULLET_LIFETIME
    
    def update(self, delta: float, level_objects: list[util.CollisionCircle]) -> bool:
        super().update(delta)
        for obj in level_objects:
            if not self.hits(obj):
                continue
            if isinstance(obj, Asteroid):
                obj.damage()
                return True
                
        self.lifetime -= delta
        return self.lifetime <= 0
    
    def draw(self, surf: Surface, view_pos: Vector2):
        screen_coord = self.get_screen_coord(surf, view_pos)
        pygame.draw.circle(surf, (0, 0, 255), screen_coord, self.radius * util.RENDER_SCALE)



class Player(DynamicCollisionCircle):
    def __init__(self):
        super().__init__(Vector2(0, 0), COLLISION_RADIUS, Vector2(0, 0))
        self.angle: float = 0.0

        self.bullets: list[PlayerBullet] = []
        self.shoot_cooldown = 0.0
    

    def get_forward_vector(self):
        vec = Vector2.from_polar((1, self.angle))
        vec.y *= -1
        return vec

    
    def handle_input(self, delta: float, keys: pygame.key.ScancodeWrapper):
        if keys[pygame.K_LEFT]:
            self.angle += ROTATE_SPEED * delta
        if keys[pygame.K_RIGHT]:
            self.angle -= ROTATE_SPEED * delta
        self.angle = util.wrap(self.angle, 0, 360)
        
        # thrust
        if keys[pygame.K_UP]:
            thrust_vector: Vector2 = self.get_forward_vector() * THRUST_STRENGTH
            self.velocity += thrust_vector * delta
            self.velocity.clamp_magnitude_ip(MAX_SPEED)
         
        # braking
        if keys[pygame.K_SPACE]:
            self.velocity.move_towards_ip(Vector2(0, 0), BRAKE_STRENGTH)
        
        # shoot
        if keys[pygame.K_x] and self.shoot_cooldown == 0:
            bullet_velocity = self.get_forward_vector() * BULLET_SPEED + self.velocity
            bullet = PlayerBullet(self.position, bullet_velocity)
            self.bullets.append(bullet)
            self.shoot_cooldown = SHOOT_COOLDOWN
            resource_manager.get_sound('shoot').play()
    

    def update(self, delta: float, level_objects: list[util.CollisionCircle]):
        super().update(delta)
        
        self.bullets = [b for b in self.bullets if not b.update(delta, level_objects)]
        self.shoot_cooldown = util.move_toward(self.shoot_cooldown, 0, delta)


    
    def draw(self, surf: Surface):
        surf_center = Vector2(surf.get_size()) / 2
        player_sprite = resource_manager.get_image('player')
        player_sprite_rotated = pygame.transform.rotate(player_sprite, self.angle)
        half_sprite_size = Vector2(player_sprite_rotated.get_size()) / 2
        surf.blit(player_sprite_rotated, surf_center-half_sprite_size)

        super().draw(surf, self.position)  # draw collision

        for bullet in self.bullets:
            bullet.draw(surf, self.position)