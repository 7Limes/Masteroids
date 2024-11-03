from globals import resource_manager, ui_handler
from ui.ui import UpgradeBox

def initialize():
    global ui_handler
    ui_handler.clear()

    upgrade_icon = resource_manager.get_image('upgrade')

    def shooting_upgrade_callback():
        print('chute upgrade')
    def brakes_upgrade_callback():
        print('break upgrade')
    def speed_upgrade_callback():
        print('i am speed upgrade')

    shooting_upgrade_box = UpgradeBox(upgrade_icon, 'Fire Rate', 20, 1, shooting_upgrade_callback)
    brakes_upgrade_box = UpgradeBox(upgrade_icon, 'Brakes', 30, 1, brakes_upgrade_callback)
    speed_upgrade_box = UpgradeBox(upgrade_icon, 'Max Speed', 40, 1, speed_upgrade_callback)

    ui_handler.elements = [shooting_upgrade_box, brakes_upgrade_box, speed_upgrade_box]