from ecs.core.components.gfx import GfxSimpleSprite, GfxAnimatedSprite
from ecs.core.components.input import GamepadButton, Input
from ecs.core.main.entity import Entity
from ecs.core.main.scene import Scene
from shmup.common.constants import *
from shmup.scripts.transitions import SwitchToScene


class Loading(Scene):

    def __init__(self, sceneMgr, sceneName):
        # Init parent class
        super().__init__(sceneMgr, SCREEN_WIDTH, SCREEN_HEIGHT, sceneName)
        # Set debug mode
        self.setDebugMode(False, False, False)
        # Add gamepad button input
        startButton = GamepadButton("start", Input.ALL_GAMEPADS_ID, "MENU")
        # Add script to go to next scene
        startScript = SwitchToScene(self, startButton, "SPLASH", "GGJ", 0.1)
        # Create Entity + Add all components
        entity = Entity("main")
        entity.addComponent(startButton)
        entity.addComponent(startScript)
        # Add entity to the scene
        self.addEntity(entity)

    def getTransitionColorOUT(self):
        return (0,0,0)
    def getTransitionTimeOUT(self):
        return 0.1
    def getTransitionColorIN(self):
        return (0,0,0)
    def getTransitionTimeIN(self):
        return 0.1
