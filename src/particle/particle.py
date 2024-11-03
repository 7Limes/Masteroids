import random
import pygame
from pygame import Vector2, Surface
import util


def uniform_with_variance(value, variance):
    return value + random.uniform(-variance, variance)


class Particle:
    def __init__(self, position: Vector2, velocity: Vector2, particle_angular_velocity: float, lifetime: float, sprite: Surface):
        self.position = position.copy()
        self.velocity = velocity.copy()

        self.particle_angular_velocity = particle_angular_velocity
        self.angle = 0.0

        self.lifetime = lifetime

        self.sprite = sprite
    

    def tickdraw(self, delta: float, surf: Surface, view_pos: Vector2) -> bool:
        self.position += self.velocity * delta
        self.angle += self.particle_angular_velocity * delta
        
        rotated_sprite = pygame.transform.rotate(self.sprite, self.angle)
        sprite_half_size = Vector2(rotated_sprite.get_size()) / 2
        screen_coordinate = util.world_to_screen(surf, view_pos, self.position, util.RENDER_SCALE)
        surf.blit(rotated_sprite, screen_coordinate - sprite_half_size)

        self.lifetime -= delta
        return self.lifetime <= 0


class ParticleEffect:
    def __init__(self, particle_count: int, position: Vector2, angle: float, angle_var: float, 
                 angular_velocity: float, angular_velocity_var: float,
                 emission_strength: float, emission_strength_var: float, duration: float, duration_var: float,
                 sprite: Surface | list[Surface], initialize: bool=True):
        self.particles: list[Particle] = []
        self.emission_vector: Vector2 = Vector2.from_polar((emission_strength, angle))

        def get_sprite():
            if isinstance(sprite, list):
                return random.choice(sprite)
            return sprite

        if initialize:
            for _ in range(particle_count):
                particle_velocity = self.emission_vector.rotate(random.uniform(-angle_var, angle_var)) * uniform_with_variance(1, emission_strength_var)
                particle_angular_velocity = uniform_with_variance(angular_velocity, angular_velocity_var)
                particle_duration = uniform_with_variance(duration, duration_var)
                p = Particle(position, particle_velocity, particle_angular_velocity, particle_duration, get_sprite())
                self.particles.append(p)


    @staticmethod
    def primitive(particle_count: int, position: Vector2, angle: float, angle_var: float, 
                 angular_velocity: float, angular_velocity_var: float,
                 emission_strength: float, emission_strength_var: float, duration: float, duration_var: float,
                 size: int, size_var, color1: tuple[int, int, int], color2: tuple[int, int, int]) -> "ParticleEffect":
        effect = ParticleEffect(particle_count, position, angle, angle_var, 
                       angular_velocity, angular_velocity_var, 
                       emission_strength, emission_strength_var, duration, duration_var, None, initialize=False)
        for _ in range(particle_count):
            particle_velocity = effect.emission_vector.rotate(random.uniform(-angle_var, angle_var)) * uniform_with_variance(1, emission_strength_var)
            particle_angular_velocity = uniform_with_variance(angular_velocity, angular_velocity_var)
            particle_duration = uniform_with_variance(duration, duration_var)
            particle_size = uniform_with_variance(size, size_var)
            particle_color = util.interpolate_color(color1, color2, random.uniform(0, 1))
            sprite = Surface((particle_size, particle_size), pygame.SRCALPHA)
            sprite.fill(particle_color)
            p = Particle(position, particle_velocity, particle_angular_velocity, particle_duration, sprite)
            effect.particles.append(p)
        return effect
        



    
    def tickdraw(self, delta: float, surf: Surface, view_pos: Vector2):
        self.particles = [p for p in self.particles if not p.tickdraw(delta, surf, view_pos)]