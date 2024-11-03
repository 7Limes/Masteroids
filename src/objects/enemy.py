import random
import math
from pygame import Vector2, Surface
import util
from globals import resource_manager, particle_effects, added_level_objects
from particle.particle import ParticleEffect
from objects.coin import Coin


ORBITER_RADIUS = 1.0
ORBITER_ACCEL = 10.0
ORBITER_VIEW_DISTANCE = 30.0

SMART_ORBITER_VIEW_DISTANCE = 25.0
SMART_ORBITER_MAX_SPEED = 25.0
SMART_ORBITER_ACCEL_BEGIN_SPEED = 100.0

LONG_ORBITER_VIEW_DISTANCE = 60.0


class Enemy(util.LevelObject):
    def __init__(self, position: Vector2, radius: float, velocity: Vector2, sprite: Surface, health: int, coins: int, score: int):
        super().__init__(position, radius, velocity, 0, sprite)
        self.health = health
        self.coins = coins
        self.score = score
        self.shake_cooldown = 0.0
    

    def destroy(self, player):
        global resource_manager, particle_effects
        self.queue_delete = True
        effect = ParticleEffect.primitive(20, self.position, 0, 360, 0, 200, 7, 1, 1, 0.2, 5, 2, (255, 50, 50), (255, 215, 0))
        particle_effects.append(effect)
        resource_manager.get_sound('explosion').play()

        for _ in range(self.coins):
            coin_position = self.position + Vector2(random.uniform(-self.radius, self.radius), random.uniform(-self.radius, self.radius)) / 2
            coin = Coin(coin_position, Vector2(random.uniform(-10, 10), random.uniform(-10, 10)))
            added_level_objects.append(coin)
        player.score += self.score
    

    def damage(self, player):
        self.health -= 1
        if self.health <= 0:
            self.destroy(player)
        else:
            resource_manager.get_sound('hit').play()
            self.shake_cooldown = 0.1
    
    def update(self, delta: float):
        super().update(delta)
        self.shake_cooldown = util.move_toward(self.shake_cooldown, 0, delta)


    def draw(self, surf: Surface, view_pos: Vector2):
        offset = Vector2(0, 0)
        if self.shake_cooldown > 0:
            offset = Vector2(random.randint(-1, 1), random.randint(-1, 1))
        super().draw(surf, view_pos, offset)


class Orbiter(Enemy):
    def __init__(self, position: util.Vector2, sprite: Surface=None, view_distance: float=ORBITER_VIEW_DISTANCE):
        if sprite is None:
            sprite = resource_manager.get_image('orbiter')
        super().__init__(position, ORBITER_RADIUS, Vector2(0, 0), sprite, 1, 1, 100)
        self.view_distance = view_distance
    

    def update(self, delta: float, player_position: Vector2):
        if self.position.distance_to(player_position) < self.view_distance:
            self.velocity += (player_position - self.position).normalize() * ORBITER_ACCEL * delta
            angle = math.atan2(self.position.y - player_position.y, self.position.x - player_position.x) * 180 / math.pi
            self.angle = angle
        else:
            self.velocity.move_towards_ip((0, 0), 0.1)
        super().update(delta)


class SmartOrbiter(Enemy):
    def __init__(self, position: Vector2):
        sprite = resource_manager.get_image('smart_orbiter')
        super().__init__(position, ORBITER_RADIUS, Vector2(0, 0), sprite, 1, 2, 150)
    

    def update(self, delta: float, player_position: Vector2):
        super().update(delta)
        if self.position.distance_to(player_position) > SMART_ORBITER_VIEW_DISTANCE:
            return
        direction = player_position - self.position
        distance = direction.length()
        desired_speed = SMART_ORBITER_MAX_SPEED * (1 - (max(0, min(distance, SMART_ORBITER_ACCEL_BEGIN_SPEED)) / SMART_ORBITER_ACCEL_BEGIN_SPEED)) ** 2
        ideal_velocity = direction.normalize() * desired_speed
        steering_strength = 3.0 * (1 - (max(0, min(distance, SMART_ORBITER_ACCEL_BEGIN_SPEED)) / SMART_ORBITER_ACCEL_BEGIN_SPEED))
        steering = (ideal_velocity - self.velocity) * delta * steering_strength

        angle = math.atan2(self.position.y - player_position.y, self.position.x - player_position.x) * -180 / math.pi + 180
        self.angle = angle
        self.velocity += steering





class LongRangeOrbiter(Orbiter):
    def __init__(self, position: Vector2):
        sprite = resource_manager.get_image('long_orbiter')
        super().__init__(position, sprite, LONG_ORBITER_VIEW_DISTANCE)