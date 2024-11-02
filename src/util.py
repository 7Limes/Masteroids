import pygame
from pygame import Vector2, Surface


RENDER_SCALE = 10


def draw_circle_alpha(surf: Surface, color: tuple[int, int, int], alpha: int, center: Vector2, radius: int):
    radius_vec = Vector2(radius, radius)
    s = Surface(radius_vec * 2, pygame.SRCALPHA)
    s.set_alpha(alpha)
    pygame.draw.circle(s, color, radius_vec, radius)
    surf.blit(s, center - radius_vec)


class CollisionCircle:
    def __init__(self, position: Vector2, radius: float):
        self.position = position
        self.radius = radius
    

    def hits(self, other: "CollisionCircle"):
        dist = self.position.distance_to(other.position)
        return dist <= self.radius + other.radius and dist >= abs(self.radius - other.radius)
    
    
    def get_bounding_box(self) -> pygame.Rect:
        return pygame.Rect(
            self.position.x - self.radius,
            self.position.y - self.radius,
            self.radius * 2,
            self.radius * 2
        )


    # Debug draw function
    def draw(self, surf: Surface, position: Vector2):
        draw_circle_alpha(surf, (0, 255, 0), 64, position, self.radius * RENDER_SCALE)


class DynamicCollisionCircle(CollisionCircle):
    def __init__(self, position: Vector2, radius: float, velocity: Vector2):
        super().__init__(position, radius)
        self.velocity = velocity
    

    def update(self, delta: float):
        self.position += self.velocity * delta


def wrap(x: float, lower: float, upper: float) -> float:
    return lower + (x - lower) % (upper - lower)


def world_to_screen(surf: Surface, view_pos: Vector2, point: Vector2, scale) -> Vector2:
    surf_width, surf_height = surf.get_size()
    center = surf_width / 2.0, surf_height / 2.0
    return (point - view_pos) * scale + center


def screen_to_world(surf: Surface, view_pos: Vector2, point: Vector2, scale) -> Vector2:
    surf_width, surf_height = surf.get_size()
    center = surf_width / 2.0, surf_height / 2.0
    return (point - center) / scale + view_pos


def get_viewport_rect(surf: Surface, view_pos: Vector2) -> pygame.Rect:
    half_viewport_size = Vector2(surf.get_size()) / 2
    return surf.get_rect().scale_by(1 / RENDER_SCALE).move(view_pos - half_viewport_size)