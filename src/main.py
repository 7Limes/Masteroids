import pygame

pygame.init()
pygame.mixer.init()

from player import Player
import level_gen
import util
from util import CollisionCircle

import globals
from globals import particle_effects


def draw_debug_label(surf: pygame.Surface, font: pygame.font.Font, text: str, position: tuple[int, int]):
    surf.blit(font.render(text, True, (255, 255, 255)), position)


def get_rendered_objects(win: pygame.Surface, view_pos: pygame.Vector2, level_objects: list[CollisionCircle]) -> list[CollisionCircle]:
    viewport = util.get_viewport_rect(win, view_pos)
    return [o for o in level_objects if viewport.colliderect(o.get_bounding_box())]


def main():
    win = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.HWSURFACE)
    pygame.display.set_caption('asteroids game')
    clock = pygame.time.Clock()

    font = pygame.font.SysFont('Arial', 15)

    globals.load_resources()

    player = Player()

    path_points, level_objects = level_gen.generate_level()

    delta: float = 0.0
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()

        player.handle_input(delta, keys)
        player.update(delta, level_objects)

        level_objects = [o for o in level_objects if not o.update(delta)]

        win.fill((0, 0, 0))

        for effect in particle_effects:
            effect.tickdraw(delta, win, player.position)

        player.draw(win)
        rendered_objects = get_rendered_objects(win, player.position, level_objects)
        for obj in rendered_objects:
            obj.draw(win, player.position)
        
        level_gen.draw_path(win, player.position, path_points)

        draw_debug_label(win, font, f'fps: {clock.get_fps():.1f}', (0, 0))
        draw_debug_label(win, font, f'pos: {player.position}', (0, 20))
        draw_debug_label(win, font, f'vel: {player.velocity}', (0, 40))
        draw_debug_label(win, font, f'angle: {player.angle:.1f}', (0, 60))
        draw_debug_label(win, font, f'drawn objs: {len(rendered_objects)}', (0, 80))


        delta = clock.tick(60) / 1000.0
        pygame.display.flip()


if __name__ == '__main__':
    main()