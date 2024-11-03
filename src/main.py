import pygame
pygame.init()
pygame.mixer.init()

from player import Player
from level_gen import level_manager, draw_path
import util
from util import CollisionCircle
import globals
from globals import particle_effects, added_level_objects, resource_manager, game_state, GameStateEnum, ui_handler, ASSETS_PATH
from resource_manager import AnimationManager
from objects.coin import Coin
from objects.enemy import Orbiter
import state


MAX_DISTANCE_FROM_PATH = 50.0
DANGER_OVERLAY_DISTANCE = 20.0


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


class GameOverHandler:
    def __init__(self):
        self.timer = 0
        self.animation_manager = AnimationManager(resource_manager.get_full_spritesheet('explosion'), 0.1)
        self.draw_player = True
        self.played_sound = False
        self.draw_game_over = False
    
    def tickdraw(self, delta: float, surf: pygame.Surface, player: Player):
        self.timer += delta
        if self.timer > 1 and self.timer < 2.8:
            if not self.played_sound:
                self.played_sound = True
                resource_manager.get_sound('deltarune_explosion').play()
            self.animation_manager.update(delta)
            surf_center = pygame.Vector2(surf.get_size()) / 2
            sprite = self.animation_manager.get_current_frame()
            surf.blit(sprite, surf_center - pygame.Vector2(sprite.get_size()) / 2)
        if self.timer > 2:
            self.draw_player = False
        if self.timer > 4:
            self.draw_game_over = True
        if self.timer > 8:
            self.reset()
            state.switch_to_menu(player)
    
    def reset(self):
        self.__init__()


def menu_update(win: pygame.Surface, font: pygame.font.Font):
    util.tile_surface(win, resource_manager.get_image('menu_bg'), 5)
    title_label = font.render('Masteroids', True, (255, 255, 255))
    title_label_pos = pygame.Vector2(win.get_size()) / 2 - pygame.Vector2(title_label.get_size()) / 2
    win.blit(title_label, title_label_pos)

    prev_selected_element = ui_handler.selected_element
    ui_handler.update()
    if prev_selected_element is None and ui_handler.selected_element:
        resource_manager.get_sound('blip').play()
    ui_handler.draw(win, font, offset=pygame.Vector2(0, title_label_pos.y + 100))



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

    # check if player is too far from path
    path_distance = util.closest_segment_distance(player.position, path_points)
    if path_distance > MAX_DISTANCE_FROM_PATH:
        state.switch_to_game_over(player)

    win.fill((0, 0, 0))

    draw_path(win, player.position, path_points)

    for effect in particle_effects:
        effect.tickdraw(delta, win, player.position)


    rendered_objects = get_rendered_objects(win, player.position, level_objects)
    for obj in rendered_objects:
        obj.draw(win, player.position)
    player.draw(win)

    if path_distance > DANGER_OVERLAY_DISTANCE:
        overlay_alpha = min(util.map_range(path_distance-DANGER_OVERLAY_DISTANCE, 0, MAX_DISTANCE_FROM_PATH-DANGER_OVERLAY_DISTANCE, 0, 255), 255)
        overlay = pygame.Surface(win.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, overlay_alpha))
        win.blit(overlay, (0, 0))


def upgrade_update(delta: float, win: pygame.Surface, title_font: pygame.font.Font, font: pygame.font.Font, player: Player):
    prev_selected_element = ui_handler.selected_element
    ui_handler.update()
    if prev_selected_element is None and ui_handler.selected_element:
        resource_manager.get_sound('blip').play()
    util.tile_surface(win, resource_manager.get_image('space_bg'), 3)
    ui_handler.draw(win, font, offset=pygame.Vector2(0, 100))

    upgrades_title = title_font.render('Upgrades', True, (255, 255, 255))
    upgrades_title_position = pygame.Vector2(win.get_size()) / 2 - pygame.Vector2(upgrades_title.get_size()) / 2
    upgrades_title_position.y = 25
    win.blit(upgrades_title, upgrades_title_position)


def game_over_update(delta: float, win: pygame.Surface, font: pygame.font.Font, player: Player, game_over_handler: GameOverHandler):
    player.selected_object = None
    player.hooked_object = None

    win.fill((0, 0, 0))
    if game_over_handler.draw_player:
        player.draw(win)
    game_over_handler.tickdraw(delta, win, player)

    if game_over_handler.draw_game_over:
        label = font.render('GAME OVER', True, (255, 255, 255))
        label_pos = pygame.Vector2(win.get_size()) / 2 - pygame.Vector2(label.get_size()) / 2
        win.blit(label, label_pos)


def main():
    global added_level_objects, particle_effects, game_state, level_manager
    win = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF | pygame.RESIZABLE | pygame.HWSURFACE)
    pygame.display.set_caption('Masteroids')
    clock = pygame.time.Clock()
    title_font = pygame.font.Font(f'{ASSETS_PATH}/font/Pixeboy.ttf', 75)
    font = pygame.font.Font(f'{ASSETS_PATH}/font/PixelTandysoft.ttf', 20)
    globals.load_resources()

    game_over_handler = GameOverHandler()

    player = Player()
    
    state.switch_to_menu(player)
    delta: float = 0.0
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        
        keys = pygame.key.get_pressed()
        if game_state.state == GameStateEnum.MENU:
            menu_update(win, title_font)
        elif game_state.state == GameStateEnum.PAUSE:
            pass
        elif game_state.state == GameStateEnum.LEVEL:
            level_update(delta, win, player, keys, level_manager.level_objects, level_manager.path_points)
        elif game_state.state == GameStateEnum.UPGRADE:
            upgrade_update(delta, win, title_font, font, player)
        elif game_state.state == GameStateEnum.GAME_OVER:
            game_over_update(delta, win, title_font, player, game_over_handler)

        draw_debug_label(win, font, f'fps: {clock.get_fps():.1f}', (0, 0))
        draw_debug_label(win, font, f'pos: {player.position}', (0, 20))
        draw_debug_label(win, font, f'coins: {player.coins}', (0, 60))

        delta = clock.tick(60) / 1000.0
        pygame.display.flip()


if __name__ == '__main__':
    main()