from ecs.core.components.gfx import GfxSimpleSprite
from ecs.core.components.input import GamepadButton, Input
from ecs.core.main.entity import Entity
from ecs.core.main.scene import Scene
from shmup.common.constants import *
from shmup.scripts.playerSelect import PlayerSelection
from shmup.scripts.transitions import SwitchToScene


class Selection(Scene):

    def __init__(self, sceneMgr, sceneName):
        # Init parent class
        super().__init__(sceneMgr, SCREEN_WIDTH, SCREEN_HEIGHT, sceneName)
        # Set debug mode
        self.setDebugMode(False, True)
        # init player list
        self.players = {}

        # Create background image
        params = {
            "filePath": f"resources/images/backgrounds/playerSelection.png",
            "size": (SCREEN_WIDTH, SCREEN_HEIGHT)
        }
        wallpaper = GfxSimpleSprite(params, 1000, "wallpaper")
        wallpaper.setPosition((SCREEN_WIDTH/2,SCREEN_HEIGHT/2))

        # Add gamepad button input
        backButton  = GamepadButton("back",  Input.ALL_GAMEPADS_ID, "VIEW")
        startButton = GamepadButton("start", Input.ALL_GAMEPADS_ID, "MENU")

        # Add script to (un)register players
        register = PlayerSelection(self.players, startButton, backButton, self, "SPLASH", "INGAME")

        # Create Entity + Add all components
        entity = Entity("main")
        entity.addComponent(wallpaper)
        entity.addComponent(startButton)
        entity.addComponent(backButton)
        entity.addComponent(register)

        # Add entity to the scene
        self.addEntity(entity)

    def getTransitionColorIN(self):
        return (0,0,0)
    def getTransitionTimeIN(self):
        return 2
    def getTransitionColorOUT(self):
        return (0,0,0)
    def getTransitionTimeOUT(self):
        return 1
