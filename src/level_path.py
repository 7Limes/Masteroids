import random
import pygame
from pygame import Vector2, Surface
import util

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
            p2_screen = util.world_to_screen(surf, view_pos, points[i+1], util.RENDER_SCALE)
            pygame.draw.line(surf, (64, 64, 64), screen_coordinate, p2_screen)
        util.draw_circle_alpha(surf, (128, 128, 128), 128, screen_coordinate, 5)
