import pygame
pygame.init()
pygame.mixer.init()

from player import Player
import level_gen
import util
from util import CollisionCircle
import globals
from globals import particle_effects, added_level_objects, resource_manager, game_state, GameStateEnum, ui_handler
from objects.coin import Coin
from objects.enemy import Orbiter
import state


def draw_debug_label(surf: pygame.Surface, font: pygame.font.Font, text: str, position: tuple[int, int]):
    surf.blit(font.render(text, True, (255, 255, 255)), position)


def get_rendered_objects(win: pygame.Surface, view_pos: pygame.Vector2, level_objects: list[CollisionCircle]) -> list[CollisionCircle]:
    viewport = util.get_viewport_rect(win, view_pos)
    return [o for o in level_objects if viewport.colliderect(o.get_bounding_box())]


def delete_queued_objects(level_objects: list[util.LevelObject]):
    i = 0
    while i < len(level_objects):
        if level_objects[i].queue_delete:
            level_objects.pop(i)
            i -= 1
        else:
            i += 1


def level_update(delta: float, win: pygame.Surface, player: Player, keys: pygame.key.ScancodeWrapper, 
                 level_objects: list[util.LevelObject], path_points: list[pygame.Vector2]):
    player.handle_input(pygame.Vector2(win.get_size()), delta, keys)
    player.update(delta, level_objects)

    for obj in level_objects:
        if isinstance(obj, (Coin, Orbiter)):
            obj.update(delta, player.position)
        else:
            obj.update(delta)
    
    delete_queued_objects(level_objects)
    level_objects.extend(added_level_objects)
    added_level_objects.clear()

    win.fill((0, 0, 0))

    for effect in particle_effects:
        effect.tickdraw(delta, win, player.position)

    rendered_objects = get_rendered_objects(win, player.position, level_objects)
    for obj in rendered_objects:
        obj.draw(win, player.position)
    player.draw(win)
    
    level_gen.draw_path(win, player.position, path_points)


def upgrade_update(delta: float, win: pygame.Surface, font: pygame.font.Font, player: Player, keys: pygame.key.ScancodeWrapper):
    prev_selected_element = ui_handler.selected_element
    ui_handler.update()
    if prev_selected_element is None and ui_handler.selected_element:
        resource_manager.get_sound('blip').play()
    util.tile_surface(win, resource_manager.get_image('space_bg'), 3)
    ui_handler.draw(win, font)


def main():
    global added_level_objects, particle_effects, game_state
    win = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.HWSURFACE)
    pygame.display.set_caption('Masteroids')
    clock = pygame.time.Clock()
    font = pygame.font.Font('assets/font/PixelTandysoft.ttf', 20)
    globals.load_resources()

    player = Player()

    difficulty = 1
    path_points, level_objects = level_gen.generate_level(difficulty)
    
    delta: float = 0.0
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()
        if game_state.state == GameStateEnum.MENU:
            pass
        elif game_state.state == GameStateEnum.PAUSE:
            pass
        elif game_state.state == GameStateEnum.LEVEL:
            level_update(delta, win, player, keys, level_objects, path_points)
        elif game_state.state == GameStateEnum.UPGRADE:
            upgrade_update(delta, win, font, player, keys)

        draw_debug_label(win, font, f'fps: {clock.get_fps():.1f}', (0, 0))
        draw_debug_label(win, font, f'pos: {player.position}', (0, 20))
        draw_debug_label(win, font, f'coins: {player.coins}', (0, 60))

        delta = clock.tick(60) / 1000.0
        pygame.display.flip()


if __name__ == '__main__':
    main()