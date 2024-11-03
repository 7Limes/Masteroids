import math
import pygame
from pygame import Vector2, Surface
from resource_manager import AnimationManager


RENDER_SCALE = 10


def draw_circle_alpha(surf: Surface, color: tuple[int, int, int], alpha: int, center: Vector2, radius: int):
    radius_vec = Vector2(radius, radius)
    s = Surface(radius_vec * 2, pygame.SRCALPHA)
    s.set_alpha(alpha)
    pygame.draw.circle(s, color, radius_vec, radius)
    surf.blit(s, center - radius_vec)


class Rect:
    def __init__(self, x: float, y: float, width: float, height: float):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def __repr__(self) -> str:
        return f'Rect({self.x:.2f}, {self.y:.2f}, {self.width:.2f}, {self.height:.2f})'
    
    @staticmethod
    def from_pygame_rect(rect: pygame.Rect):
        return Rect(*rect.topleft, *rect.size)

    def colliderect(self, other: "Rect"):
        return not (
            self.x + self.width <= other.x or \
            other.x + other.width <= self.x or \
            self.y + self.height <= other.y or \
            other.y + other.height <= self.y
        )

    def scale_by(self, factor: float) -> "Rect":
        return Rect(self.x, self.y, self.width * factor, self.height * factor)

    def move(self, move_vector: Vector2) -> "Rect":
        return Rect(self.x + move_vector.x, self.y + move_vector.y, self.width, self.height)


class CollisionCircle:
    def __init__(self, position: Vector2, radius: float):
        self.position = Vector2(position)
        self.radius = radius
    

    def hits(self, other: "CollisionCircle"):
        dist = self.position.distance_to(other.position)
        return dist <= self.radius + other.radius
    

    def hits_point(self, point: Vector2):
        return self.position.distance_to(point) <= self.radius
    
    
    def get_bounding_box(self) -> Rect:
        return Rect(
            self.position.x - self.radius,
            self.position.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )


    def get_screen_coord(self, surf: Surface, view_pos: Vector2):
        return world_to_screen(surf, view_pos, self.position, RENDER_SCALE)


    # Debug draw function
    def draw(self, surf: Surface, view_pos: Vector2):
        screen_coord = self.get_screen_coord(surf, view_pos)
        draw_circle_alpha(surf, (0, 255, 0), 64, screen_coord, self.radius * RENDER_SCALE)


class DynamicCollisionCircle(CollisionCircle):
    def __init__(self, position: Vector2, radius: float, velocity: Vector2):
        super().__init__(position, radius)
        self.velocity = Vector2(velocity)
    

    def update(self, delta: float):
        self.position += self.velocity * delta


def wrap(x: float, lower: float, upper: float) -> float:
    return lower + (x - lower) % (upper - lower)


def move_toward(current: float, target: float, delta: float) -> float:
    direction = (target - current) > 0
    adjustment = min(abs(target - current), delta)
    return current + adjustment if direction else current - adjustment


def world_to_screen(surf: Surface, view_pos: Vector2, point: Vector2, scale) -> Vector2:
    surf_width, surf_height = surf.get_size()
    center = surf_width / 2.0, surf_height / 2.0
    return (point - view_pos) * scale + center


def screen_to_world(surf: Surface, view_pos: Vector2, point: Vector2, scale) -> Vector2:
    surf_width, surf_height = surf.get_size()
    center = surf_width / 2.0, surf_height / 2.0
    return (point - center) / scale + view_pos


def get_viewport_rect(surf: Surface, view_pos: Vector2) -> Rect:
    viewport = Rect.from_pygame_rect(surf.get_rect()).scale_by(1 / RENDER_SCALE)
    half_viewport_size = Vector2(viewport.width, viewport.height) / 2
    return viewport.move(view_pos - half_viewport_size)


class LevelObject(DynamicCollisionCircle):
    def __init__(self, position: Vector2, radius: float, velocity: Vector2, angular_velocity: float, sprite: Surface):
        super().__init__(position, radius, velocity)
        self.angular_velocity = angular_velocity
        self.angle = 0.0
        self.sprite = sprite

        scaled_sprite_size = radius * 2 * RENDER_SCALE
        self.sprite = pygame.transform.scale(sprite, Vector2(scaled_sprite_size, scaled_sprite_size))
        self.queue_delete = False


    def update(self, delta: float):
        super().update(delta)
        self.angle += self.angular_velocity * delta


    def draw(self, surf: Surface, view_pos: Vector2, screen_coord_offset: Vector2=Vector2(0, 0)):
        screen_coord = self.get_screen_coord(surf, view_pos) + screen_coord_offset
        blit_sprite = self.sprite
        if self.angle != 0:
            blit_sprite = pygame.transform.rotate(self.sprite, self.angle)
        
        blit_position = screen_coord - Vector2(blit_sprite.get_size()) / 2
        surf.blit(blit_sprite, blit_position)


class AnimatedLevelObject(LevelObject):
    def __init__(self, position: Vector2, radius: float, velocity: Vector2, angular_velocity: float, sprites: list[Surface], frame_duration: float):
        super().__init__(position, radius, velocity, angular_velocity, sprites[0])
        scaled_sprite_size = radius * 2 * RENDER_SCALE
        scaled_sprites = []
        for sprite in sprites:
            scaled_sprite = pygame.transform.scale(sprite, Vector2(scaled_sprite_size, scaled_sprite_size))
            scaled_sprites.append(scaled_sprite)
        self.animation_manager = AnimationManager(scaled_sprites, frame_duration)
    

    def update(self, delta: float):
        self.animation_manager.update(delta)
        self.sprite = self.animation_manager.get_current_frame()
        super().update(delta)
    

def tile_surface(destination_surf: Surface, source_surf: Surface, tile_scale: float=1.0):
    if tile_scale != 1.0:
        source_surf = pygame.transform.scale_by(source_surf, tile_scale)
    dest_width, dest_height = destination_surf.get_size()
    source_width, source_height = source_surf.get_size()
    tiles_x = max(1, math.ceil(dest_width / source_width))
    tiles_y = max(1, math.ceil(dest_height / source_height))
    for i in range(tiles_y):
        for j in range(tiles_x):
            blit_pos = (j*source_width, i*source_height)
            destination_surf.blit(source_surf, blit_pos)


def interpolate_color(color1: tuple[int, int, int], color2: tuple[int, int, int], t: float) -> tuple[int, int, int]:
    if not (0 <= t <= 1):
        raise ValueError("The value of t must be between 0 and 1.")

    def interpolate_channel(c1, c2, t):
        return int(round(c1 + (c2 - c1) * t))
    
    r1, g1, b1 = color1
    r2, g2, b2 = color2

    r = interpolate_channel(r1, r2, t)
    g = interpolate_channel(g1, g2, t)
    b = interpolate_channel(b1, b2, t)

    return (r, g, b)