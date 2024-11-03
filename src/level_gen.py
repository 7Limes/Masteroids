import random
import math
import pygame
from pygame import Vector2, Surface
import util
from objects.asteroid import Asteroid, CoinAsteroid
from objects.enemy import Orbiter, SmartOrbiter
from objects.level_end import LevelEnd


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


def generate_asteroid(position: Vector2) -> Asteroid:
    ast_size = random.randint(4, 12) / 2.0
    if random.randrange(0, 7) == 0:
        return CoinAsteroid(position, ast_size, Vector2(random.uniform(-1, 1), random.uniform(-1, 1)), random.uniform(-10, 10))
    return Asteroid(position, ast_size, Vector2(random.uniform(-1, 1), random.uniform(-1, 1)), random.uniform(-10, 10))


def generate_object(position: Vector2, difficulty: float) -> util.LevelObject:
    orbiter_chance = -4*difficulty+90 if difficulty < 10 else 50
    r = random.randrange(0, 100)
    if r < orbiter_chance:
        return generate_asteroid(position)
    return SmartOrbiter(position)


def max_object_distance(difficulty: int):
    if difficulty < 10:
        return math.floor(-10 * math.sqrt(difficulty) + 55)
    return 1 / (difficulty-9) + 22.38


# Creates a path and populates it with objects.
def generate_level(difficulty: int) -> tuple[list[Vector2], list[util.LevelObject]]:
    amount_points = math.floor(0.5*difficulty + 8) if difficulty < 14 else 15
    average_amount_objects = math.floor(4 * math.sqrt(difficulty))
    object_distance = max_object_distance(difficulty)

    end_point = Vector2.from_polar((random.uniform(350, 450), random.uniform(0, 360)))
    amount_points += random.randrange(-1, 1)
    path_points = generate_path(Vector2(0, 0), end_point, amount_points, 45, 3)


    level_objects: list[util.LevelObject] = [
        LevelEnd(end_point)
    ]
    for p1, p2 in zip(path_points[1:], path_points[2:]):
        line_length = p1.distance_to(p2)
        shift_vector = (p2 - p1).normalize()
        perp_vector = shift_vector.rotate(90)
        for i in range(average_amount_objects + random.randint(-1, 1)):
            obj_line_position = shift_vector * random.uniform(0, line_length) + p1
            obj_position = obj_line_position + (perp_vector * random.uniform(-object_distance, object_distance))
            if obj_position.distance_to((0, 0)) < 10:
                continue
            obj = generate_object(obj_position, difficulty)
            level_objects.append(obj)
    return (path_points, level_objects)



class LevelManager:
    def __init__(self):
        self.difficulty = 0
        self.path_points: list[Vector2] = []
        self.level_objects: list[util.LevelObject] = []

    def load_next_level(self):
        self.difficulty += 1
        self.path_points, self.level_objects = generate_level(self.difficulty)
    
    def reset(self):
        self.__init__()


level_manager = LevelManager()