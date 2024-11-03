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
from objects.enemy import Enemy
import state
from stars import StarfieldBackground


MAX_DISTANCE_FROM_PATH = 60.0
DANGER_OVERLAY_DISTANCE = 30.0
OUT_OF_BOUNDS_FORCE_STRENGTH = 5.0

def draw_label(surf: pygame.Surface, font: pygame.font.Font, text: str, position: tuple[int, int]):
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
            player.full_reset()
            state.switch_to_menu(player)
    
    def reset(self):
        self.__init__()


def menu_update(win: pygame.Surface, font: pygame.font.Font):
    util.tile_surface(win, resource_manager.get_image('menu_bg'), 5)
    title_label = font.render('Masteroids', True, (255, 255, 255))
    title_label_pos = pygame.Vector2(win.get_size()) / 2 - pygame.Vector2(title_label.get_size()) / 2 + pygame.Vector2(0, -200)
    win.blit(title_label, title_label_pos)

    prev_selected_element = ui_handler.selected_element
    ui_handler.update()
    if prev_selected_element is None and ui_handler.selected_element:
        resource_manager.get_sound('blip').play()
    ui_handler.draw(win, font, offset=pygame.Vector2(0, title_label_pos.y + 100))



def level_update(delta: float, win: pygame.Surface, font: pygame.font.Font, player: Player, keys: pygame.key.ScancodeWrapper, 
                 level_objects: list[util.LevelObject], path_points: list[pygame.Vector2], stars_background: StarfieldBackground):
    player.handle_input(pygame.Vector2(win.get_size()), delta, keys)
    player.update(delta, level_objects)

    for obj in level_objects:
        if isinstance(obj, (Coin, Enemy)):
            obj.update(delta, player.position)
        else:
            obj.update(delta)
    
    delete_queued_objects(level_objects)
    level_objects.extend(added_level_objects)
    added_level_objects.clear()

    # check if player is too far from path
    path_distance, path_point = util.closest_segment_point_distance(player.position, path_points)
    if path_distance > MAX_DISTANCE_FROM_PATH:
        force_vec = (path_point - player.position).normalize() * (path_distance-MAX_DISTANCE_FROM_PATH) * OUT_OF_BOUNDS_FORCE_STRENGTH
        player.velocity += force_vec * delta

    win.fill((0, 0, 0))

    stars_background.update(player.position)
    stars_background.draw(win)

    if path_distance > DANGER_OVERLAY_DISTANCE:
        overlay_alpha = min(util.map_range(path_distance-DANGER_OVERLAY_DISTANCE, 0, MAX_DISTANCE_FROM_PATH-DANGER_OVERLAY_DISTANCE, 0, 255), 255)
        overlay = pygame.Surface(win.get_size(), pygame.SRCALPHA)
        overlay.fill((5, 5, 15, overlay_alpha))
        win.blit(overlay, (0, 0))
    
    draw_path(win, player.position, path_points)

    for effect in particle_effects:
        effect.tickdraw(delta, win, player.position)


    rendered_objects = get_rendered_objects(win, player.position, level_objects)
    for obj in rendered_objects:
        obj.draw(win, player.position)
    player.draw(win)

    
    draw_label(win, font, f'Score: {player.score}', (5, 5))
    coin_icon = pygame.transform.scale_by(resource_manager.get_spritesheet_image('coin', 0), 2)
    win.blit(coin_icon, (5, 30))
    draw_label(win, font, f'x {player.coins}', (30, 23))


def upgrade_update(win: pygame.Surface, title_font: pygame.font.Font, font: pygame.font.Font, player: Player):
    prev_selected_element = ui_handler.selected_element
    ui_handler.update()
    if prev_selected_element is None and ui_handler.selected_element:
        resource_manager.get_sound('blip').play()
    util.tile_surface(win, resource_manager.get_image('space_bg'), 3)
    ui_handler.draw(win, font, offset=pygame.Vector2(0, 150))

    upgrades_title = title_font.render('Upgrades', True, (255, 255, 255))
    upgrades_title_position = pygame.Vector2(win.get_size()) / 2 - pygame.Vector2(upgrades_title.get_size()) / 2
    upgrades_title_position.y = 25
    win.blit(upgrades_title, upgrades_title_position)

    coin_icon = pygame.transform.scale_by(resource_manager.get_spritesheet_image('coin', 0), 2)
    screen_center_x = win.get_size()[0] / 2
    win.blit(coin_icon, (screen_center_x-27, 107))
    draw_label(win, font, f'x {player.coins}', (screen_center_x, 100))


def game_over_update(delta: float, win: pygame.Surface, title_font: pygame.font.Font, font: pygame.font.Font, player: Player, game_over_handler: GameOverHandler):
    player.selected_object = None
    player.hooked_object = None

    win.fill((0, 0, 0))
    if game_over_handler.draw_player:
        player.draw(win)
    game_over_handler.tickdraw(delta, win, player)

    if game_over_handler.draw_game_over:
        label = title_font.render('GAME OVER', True, (255, 255, 255))
        win_half_size = pygame.Vector2(win.get_size()) / 2
        label_pos = win_half_size - pygame.Vector2(label.get_size()) / 2
        score_label = font.render(f'Score: {player.score}', True, (255, 255, 255))
        score_label_pos = win_half_size - pygame.Vector2(score_label.get_size()) / 2 + pygame.Vector2(0, 50)
        level_label = font.render(f'You made it to level {level_manager.difficulty}', True, (255, 255, 255))
        level_label_pos = win_half_size - pygame.Vector2(level_label.get_size()) / 2 + pygame.Vector2(0, 80)
        win.blit(label, label_pos)
        win.blit(score_label, score_label_pos)
        win.blit(level_label, level_label_pos)


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

    stars_background = StarfieldBackground((1280, 720))
    
    state.switch_to_menu(player)
    delta: float = 0.0
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.WINDOWRESIZED:
                stars_background.resize(win.get_size())
        
        keys = pygame.key.get_pressed()
        if game_state.state == GameStateEnum.MENU:
            menu_update(win, title_font)
        elif game_state.state == GameStateEnum.PAUSE:
            pass
        elif game_state.state == GameStateEnum.LEVEL:
            level_update(delta, win, font, player, keys, level_manager.level_objects, level_manager.path_points, stars_background)
        elif game_state.state == GameStateEnum.UPGRADE:
            upgrade_update(win, title_font, font, player)
        elif game_state.state == GameStateEnum.GAME_OVER:
            game_over_update(delta, win, title_font, font, player, game_over_handler)

        delta = clock.tick(60) / 1000.0
        pygame.display.flip()


if __name__ == '__main__':
    main()