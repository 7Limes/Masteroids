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


def calculate_upgrade_cost(level: int) -> int:
    return int(2.5 * (level+1.5)**2 + 14.375)


def purchase_logic(player, upgrade_id: str, upgrade_box: UpgradeBox):
    if player.coins > upgrade_box.cost:
        player.coins -= upgrade_box.cost
        player.upgrades[upgrade_id] += 1
        upgrade_box.cost = calculate_upgrade_cost(player.upgrades[upgrade_id])
        upgrade_box.level += 1
        resource_manager.get_sound('upgrade').play()
    else:
        resource_manager.get_sound('hit').play()


def initialize_upgrade_menu(player):
    global ui_handler
    ui_handler.clear()

    def fire_rate_upgrade_callback():
        purchase_logic(player, 'fire_rate', fire_rate_upgrade_box)
    def brakes_upgrade_callback():
        purchase_logic(player, 'brakes', brakes_upgrade_box)
    def thrust_upgrade_callback():
        purchase_logic(player, 'thrust', thrust_upgrade_box)
    def continue_callback():
        switch_to_level(player)

    fire_rate_icon = resource_manager.get_image('fire_rate_icon')
    brakes_icon = resource_manager.get_image('brakes_icon')
    thrust_icon = resource_manager.get_image('thrust_icon')

    fire_rate_level = player.upgrades['fire_rate']
    brakes_level = player.upgrades['brakes']
    thrust_level = player.upgrades['thrust']

    fire_rate_cost = calculate_upgrade_cost(fire_rate_level)
    brakes_cost = calculate_upgrade_cost(brakes_level)
    thrust_cost = calculate_upgrade_cost(thrust_level)

    fire_rate_upgrade_box = UpgradeBox(Vector2(100, 100), UPGRADE_BOX_SIZE, fire_rate_upgrade_callback, fire_rate_icon, 'Fire Rate', fire_rate_cost, fire_rate_level+1)
    brakes_upgrade_box = UpgradeBox(Vector2(100, 250), UPGRADE_BOX_SIZE, brakes_upgrade_callback, brakes_icon, 'Brakes', brakes_cost, brakes_level+1)
    thrust_upgrade_box = UpgradeBox(Vector2(100, 300), UPGRADE_BOX_SIZE, thrust_upgrade_callback, thrust_icon, 'Thrust', thrust_cost, thrust_level+1)
    continue_button = LabelButton(Vector2(100, 450), UPGRADE_BOX_SIZE, continue_callback, 'Continue')

    ui_handler.elements.extend([fire_rate_upgrade_box, brakes_upgrade_box, thrust_upgrade_box, continue_button])


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
    player.full_reset()
    game_state.set_state(GameStateEnum.GAME_OVER)


def switch_to_menu(player):
    initialize_main_menu(player)
    game_state.set_state(GameStateEnum.MENU)