import random
from pygame import Vector2, Surface
import util


def uniform_with_variance(value, variance):
    return value + random.uniform(-variance, variance)


class Particle:
    def __init__(self, position: Vector2, velocity: Vector2, lifetime: float, sprite: Surface):
        self.position = position.copy()
        self.velocity = velocity.copy()
        self.lifetime = lifetime

        self.sprite = sprite
        self.sprite_half_size = Vector2(sprite.get_size()) / 2
    

    def tickdraw(self, delta: float, surf: Surface, view_pos: Vector2) -> bool:
        self.position += self.velocity * delta
        screen_coordinate = util.world_to_screen(surf, view_pos, self.position, util.RENDER_SCALE)
        surf.blit(self.sprite, screen_coordinate - self.sprite_half_size)

        self.lifetime -= delta
        return self.lifetime <= 0


class ParticleEffect:
    def __init__(self, particle_count: int, position: Vector2, angle: float, angle_var: float, 
                 emission_strength: float, emission_strength_var: float, duration: float, duration_var: float,
                 sprite: Surface):
        self.particles: list[Particle] = []
        self.emission_vector: Vector2 = Vector2.from_polar((emission_strength, angle))
        self.sprite = sprite

        for i in range(particle_count):
            particle_velocity = self.emission_vector.rotate(random.uniform(-angle_var, angle_var)) * uniform_with_variance(1, emission_strength_var)
            particle_duration = uniform_with_variance(duration, duration_var)
            p = Particle(position, particle_velocity, particle_duration, sprite)
            self.particles.append(p)

    
    def tickdraw(self, delta: float, surf: Surface, view_pos: Vector2):
        self.particles = [p for p in self.particles if not p.tickdraw(delta, surf, view_pos)]