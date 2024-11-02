import random
import pygame
from pygame import Vector2, Surface
import util

from hazards.asteroid import Asteroid

def generate_path(start: Vector2, end: Vector2, amount_points: int, angle_variance: float, length_variance: float) -> list[Vector2]:
    points: list[Vector2] = [start]
    average_line_length = start.distance_to(end) / (amount_points + 1)
    current_point = Vector2(start)
    for i in range(amount_points):
        towards_end = (end - current_point).normalize()
        shift_vector = towards_end.rotate(random.uniform(-angle_variance, angle_variance))
        shift_vector *= average_line_length + random.uniform(-length_variance, length_variance)
        current_point += shift_vector
        points.append(Vector2(current_point))
    points.append(end)
    return points


def draw_path(surf: Surface, view_pos: Vector2, points: list[Vector2]):
    for i, point in enumerate(points):
        screen_coordinate = util.world_to_screen(surf, view_pos, point, util.RENDER_SCALE)
        if i < len(points)-1:
            p2_screen_coordinate = util.world_to_screen(surf, view_pos, points[i+1], util.RENDER_SCALE)
            pygame.draw.line(surf, (64, 64, 64), screen_coordinate, p2_screen_coordinate)
        util.draw_circle_alpha(surf, (128, 128, 128), 128, screen_coordinate, 5)


# Creates a path and populates it with objects.
def generate_level() -> tuple[list[Vector2], list[util.CollisionCircle]]:
    end_point = Vector2.from_polar((random.uniform(350, 450), random.uniform(0, 360)))
    amount_points = random.randrange(7, 15)
    path_points = generate_path(Vector2(0, 0), end_point, amount_points, 45, 3)

    level_objects: list[util.CollisionCircle] = []
    for p1, p2 in zip(path_points[1:], path_points[2:]):
        line_length = p1.distance_to(p2)
        shift_vector = (p2 - p1).normalize()
        perp_vector = shift_vector.rotate(90)
        for i in range(random.randrange(7, 15)):
            obj_line_position = shift_vector * random.uniform(0, line_length) + p1
            obj_position = obj_line_position + (perp_vector * random.uniform(-40, 40))
            obj = Asteroid(obj_position, random.randint(4, 12) / 2.0, Vector2(random.uniform(-1, 1), random.uniform(-1, 1)))
            level_objects.append(obj)

    return (path_points, level_objects)