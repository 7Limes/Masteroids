from globals import game_state, GameStateEnum
import ui.ui_init as ui_init

def switch_to_level():
    pass


def switch_to_upgrade():
    global game_state
    ui_init.initialize()
    game_state.set_state(GameStateEnum.UPGRADE)