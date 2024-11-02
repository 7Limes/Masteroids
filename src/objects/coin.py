from pygame import Vector2
import util
from globals import resource_manager


RADIUS = 0.75
ANIMATION_FRAME_DURATION = 0.5
MAGNETIZE_MAX_SPEED = 100.0
MAGNETIZE_ACCEL_BEGIN_SPEED = 200.0


class Coin(util.AnimatedLevelObject):
    def __init__(self, position: Vector2, velocity: Vector2):
        coin_sprites = resource_manager.get_full_spritesheet('coin')
        super().__init__(position, RADIUS, velocity, coin_sprites, ANIMATION_FRAME_DURATION)
        self.magnetize_delay = 0.5
    

    def update(self, delta: float, player_position: Vector2):
        self.magnetize_delay = util.move_toward(self.magnetize_delay, 0, delta)
        if self.magnetize_delay > 0:
            self.position += self.velocity * delta
            self.velocity *= 0.95
        else:
            direction = player_position - self.position
            distance = direction.length()
            
            # Invert the speed calculation - slower when far, faster when close
            desired_speed = MAGNETIZE_MAX_SPEED * (1 - (max(0, min(distance, MAGNETIZE_ACCEL_BEGIN_SPEED)) / MAGNETIZE_ACCEL_BEGIN_SPEED)) ** 2
            
            ideal_velocity = direction.normalize() * desired_speed
            
            # Increase steering strength when closer to make turns sharper
            steering_strength = 3.0 * (1 - (max(0, min(distance, MAGNETIZE_ACCEL_BEGIN_SPEED)) / MAGNETIZE_ACCEL_BEGIN_SPEED))
            steering = (ideal_velocity - self.velocity) * delta * steering_strength
            
            self.velocity += steering
            super().update(delta)