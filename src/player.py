import math
import pygame
from pygame import Vector2, Surface

import util
from util import DynamicCollisionCircle
from objects.asteroid import Asteroid
from objects.coin import Coin
from objects.enemy import Enemy
from objects.level_end import LevelEnd
import globals
from globals import resource_manager, particle_effects
import state
from particle.particle import ParticleEffect


ROTATE_SPEED = 180.0
MAX_SPEED = 30.0
COLLISION_RADIUS = 0.75

BULLET_RADIUS = 0.2
BULLET_SPEED = 30.0
BULLET_LIFETIME = 3.0

HOOK_MAX_DISTANCE = 30.0

def ray_intersect_circle(ray_origin: Vector2, ray_angle: float, circle_center: Vector2, circle_radius: float) -> bool:
    # Ensure the ray_direction is normalized
    ray_direction = Vector2.from_polar((1, ray_angle))

    # Vector from the ray origin to the circle center
    to_circle = circle_center - ray_origin

    # Project the circle center onto the ray direction using dot product
    proj_length = to_circle.dot(ray_direction)

    # Closest point on the ray to the circle center
    closest_point = ray_origin + proj_length * ray_direction

    # Distance from the closest point to the circle center
    distance_to_circle = closest_point.distance_to(circle_center)

    # Determine if the ray intersects the circle
    within_radius = distance_to_circle < circle_radius

    # Check if projection is along the ray's positive direction and within the circle's radius.
    return proj_length >= 0 and within_radius


class PlayerBullet(DynamicCollisionCircle):
    def __init__(self, position: Vector2, velocity: Vector2, parent: "Player"):
        super().__init__(position, BULLET_RADIUS, velocity)
        self.lifetime = BULLET_LIFETIME
        self.parent: Player = parent
    
    def update(self, delta: float, level_objects: list[util.LevelObject]) -> bool:
        super().update(delta)
        for obj in level_objects:
            if not self.hits(obj):
                continue
            if isinstance(obj, (Asteroid, Enemy)):
                obj.damage(self.parent)
                return True
                
        self.lifetime -= delta
        return self.lifetime <= 0
    
    def draw(self, surf: Surface, view_pos: Vector2):
        screen_coord = self.get_screen_coord(surf, view_pos)
        pygame.draw.circle(surf, (255, 255, 255), screen_coord, self.radius * util.RENDER_SCALE)



class Player(DynamicCollisionCircle):
    def __init__(self):
        super().__init__(Vector2(0, 0), COLLISION_RADIUS, Vector2(0, 0))
        self.angle: float = 0.0

        self.bullets: list[PlayerBullet] = []
        self.shoot_cooldown = 0.0

        self.coins: int = 0
        self.score: int = 0

        self.selected_object: util.LevelObject | None = None
        self.hooked_object: util.LevelObject | None = None
        self.hook_distance: float = 0.0

        self.upgrades = {
            'fire_rate': 0,
            'brakes': 0,
            'thrust': 0,
        }
    

    def get_forward_vector(self):
        vec = Vector2.from_polar((1, self.angle))
        vec.y *= -1
        return vec

    
    def handle_input(self, screen_size: Vector2, delta: float, keys: pygame.key.ScancodeWrapper):
        if globals.keyboard_aim:
            if keys[pygame.K_LEFT]:
                self.angle += ROTATE_SPEED * delta
            if keys[pygame.K_RIGHT]:
                self.angle -= ROTATE_SPEED * delta
            self.angle = util.wrap(self.angle, 0, 360)

            thrust = keys[pygame.K_UP]
            brake = keys[pygame.K_DOWN]
            shoot = keys[pygame.K_z]
            hook = keys[pygame.K_x]
        else:  # mouse aiming
            mouse_position = Vector2(pygame.mouse.get_pos())
            self.angle = math.atan2(mouse_position.y - screen_size.y/2, mouse_position.x - screen_size.x/2) * -180 / math.pi

            thrust = keys[pygame.K_w]
            brake = keys[pygame.K_s]
            shoot, _, hook = pygame.mouse.get_pressed()
        
        
        # thrust
        if thrust:
            forward = self.get_forward_vector()
            thrust_level = self.upgrades['thrust']
            thrust_strength = 7.5*thrust_level + 20
            thrust_vector: Vector2 = forward * thrust_strength
            self.velocity += thrust_vector * delta
            self.velocity.clamp_magnitude_ip(MAX_SPEED)

            effect_position = -forward * 1.25 + self.position
            effect = ParticleEffect.primitive(5, effect_position, self.angle+180, 20, 0, 150, 7, 1, 0.3, 0.1, 5, 2, (255, 50, 50), (255, 215, 0))
            particle_effects.append(effect)
         
        # braking
        if brake:
            brake_level = self.upgrades['brakes']
            brake_strength = 0.2*brake_level + 0.7
            self.velocity.move_towards_ip(Vector2(0, 0), brake_strength)
        
        # shoot
        if shoot and self.shoot_cooldown == 0:
            bullet_velocity = self.get_forward_vector() * BULLET_SPEED + self.velocity
            bullet = PlayerBullet(self.position, bullet_velocity, self)
            self.bullets.append(bullet)
            fire_rate_level = self.upgrades['fire_rate']
            self.shoot_cooldown = -0.05*fire_rate_level + 0.4
            resource_manager.get_sound('shoot').play()
        
        # hook
        if hook:
            if self.selected_object is not None and self.hooked_object is None:
                self.hooked_object = self.selected_object
                self.hook_distance = self.position.distance_to(self.hooked_object.position)
                resource_manager.get_sound('hook').play()
        else:
            self.hooked_object = None
    

    def hook_update(self, delta: float):
        if self.hooked_object == None:
            return

        displacement = self.position - self.hooked_object.position
        distance = displacement.length()
        
        # Only apply swing physics if rope is taut
        if distance >= self.hook_distance:
            # Normalize the displacement vector
            normal = displacement / distance
            # Calculate tangential direction (perpendicular to normal)
            tangent = Vector2(-normal.y, normal.x)
            # Project current velocity onto tangent to preserve momentum
            projected_velocity = tangent * self.velocity.dot(tangent)
            # Apply tension force to keep player at rope length
            tension = normal * (distance - self.hook_distance)
            # Update velocity with tension and dampening
            self.velocity = projected_velocity - tension + normal
    

    def update(self, delta: float, level_objects: list[util.LevelObject]):
        super().update(delta)

        raycast_hit_objects: list[util.LevelObject] = []
        for obj in level_objects:
            if isinstance(obj, Asteroid) and ray_intersect_circle(self.position, 360-self.angle, obj.position, obj.radius):
                raycast_hit_objects.append(obj)
            
            if not self.hits(obj):
                continue
            if isinstance(obj, Coin):
                resource_manager.get_sound('coin').play()
                obj.queue_delete = True
                self.coins += 1
            elif isinstance(obj, LevelEnd):
                resource_manager.get_sound('end_level').play()
                state.switch_to_upgrade(self)
            else:
                self.bullets.clear()
                state.switch_to_game_over(self)

        
        if raycast_hit_objects:
            self.selected_object = min(raycast_hit_objects, key=lambda o: self.position.distance_squared_to(o.position))
            if self.position.distance_to(self.selected_object.position) > HOOK_MAX_DISTANCE:
                self.selected_object = None
        else:
            self.selected_object = None

        self.hook_update(delta)
        
        self.bullets = [b for b in self.bullets if not b.update(delta, level_objects)]
        self.shoot_cooldown = util.move_toward(self.shoot_cooldown, 0, delta)
    

    def reset_objects(self):
        self.bullets.clear()
        self.selected_object = None
        self.hooked_object = None


    def reset_position(self):
        self.position = Vector2(0, 0)
        self.velocity = Vector2(0, 0)
        self.angle = 0.0
    

    def full_reset(self):
        self.__init__()

    
    def draw(self, surf: Surface):
        surf_center = Vector2(surf.get_size()) / 2
        player_sprite = resource_manager.get_image('player')
        player_sprite_rotated = pygame.transform.rotate(player_sprite, self.angle)
        half_sprite_size = Vector2(player_sprite_rotated.get_size()) / 2
        surf.blit(player_sprite_rotated, surf_center-half_sprite_size)
        if self.selected_object is not None:
            selected_screen_coord = util.world_to_screen(surf, self.position, self.selected_object.position, util.RENDER_SCALE)
            pygame.draw.circle(surf, (80, 80, 80), selected_screen_coord, 5)
            pygame.draw.circle(surf, (80, 80, 80), selected_screen_coord, 8, 1)
        if self.hooked_object is not None:
            hooked_screen_coord = util.world_to_screen(surf, self.position, self.hooked_object.position, util.RENDER_SCALE)
            pygame.draw.line(surf, (128, 128, 128), surf_center, hooked_screen_coord)

        for bullet in self.bullets:
            bullet.draw(surf, self.position)