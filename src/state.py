from globals import game_state, GameStateEnum, resource_manager
from pygame import Vector2
from globals import resource_manager, ui_handler, particle_effects, added_level_objects
from ui.ui import UpgradeBox, LabelButton
from level_gen import level_manager


UPGRADE_BOX_SIZE = Vector2(500, 100)


def initialize_main_menu(player):
    global ui_handler
    ui_handler.clear()

    def start_callback():
        switch_to_level(player)

    start_button = LabelButton(Vector2(100, 100), Vector2(400, 80), start_callback, 'Start')
    ui_handler.elements.append(start_button)


def initialize_upgrade_menu(player):
    global ui_handler
    ui_handler.clear()

    def shooting_upgrade_callback():
        print('chute upgrade')
    def brakes_upgrade_callback():
        print('break upgrade')
    def thrust_upgrade_callback():
        print('i am speed upgrade')
    def continue_callback():
        switch_to_level(player)

    fire_rate_icon = resource_manager.get_image('fire_rate_icon')
    brakes_icon = resource_manager.get_image('brakes_icon')
    thrust_icon = resource_manager.get_image('thrust_icon')
    shooting_upgrade_box = UpgradeBox(Vector2(100, 100), UPGRADE_BOX_SIZE, shooting_upgrade_callback, fire_rate_icon, 'Fire Rate', 20, 1)
    brakes_upgrade_box = UpgradeBox(Vector2(100, 250), UPGRADE_BOX_SIZE, brakes_upgrade_callback, brakes_icon, 'Brakes', 30, 1)
    thrust_upgrade_box = UpgradeBox(Vector2(100, 300), UPGRADE_BOX_SIZE, thrust_upgrade_callback, thrust_icon, 'Thrust', 40, 1)
    continue_button = LabelButton(Vector2(100, 450), UPGRADE_BOX_SIZE, continue_callback, 'Continue')

    ui_handler.elements.extend([shooting_upgrade_box, brakes_upgrade_box, thrust_upgrade_box, continue_button])


def switch_to_level(player):
    player.reset_position()
    particle_effects.clear()
    added_level_objects.clear()
    level_manager.load_next_level()
    game_state.set_state(GameStateEnum.LEVEL)


def switch_to_upgrade(player):
    global game_state
    initialize_upgrade_menu(player)
    game_state.set_state(GameStateEnum.UPGRADE)


def switch_to_game_over(player):
    resource_manager.get_sound('death').play()
    player.coins = 0
    game_state.set_state(GameStateEnum.GAME_OVER)


def switch_to_menu(player):
    initialize_main_menu(player)
    game_state.set_state(GameStateEnum.MENU)