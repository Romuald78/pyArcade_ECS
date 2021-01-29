from ecs.core.components.gfx import GfxSimpleSprite, GfxAnimatedSprite
from ecs.core.components.input import GamepadButton, Input
from ecs.core.main.entity import Entity
from ecs.core.main.scene import Scene
from shmup.common.constants import *
from shmup.scripts.transitions import SwitchToScene


class DisplayGGJ(Scene):

    def __init__(self, sceneMgr, sceneName):
        # Init parent class
        super().__init__(sceneMgr, SCREEN_WIDTH, SCREEN_HEIGHT, sceneName)
        # Set debug mode
        self.setDebugMode(False, False, False)
        # Create background image
        params = {
            "filePath": f"resources/images/backgrounds/ggj2021.png",
            "size": (SCREEN_WIDTH, SCREEN_HEIGHT),
            "position": (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            "textureName": f"wallPaper{self.getID()}",
            "spriteBox": (1, 1, SCREEN_WIDTH, SCREEN_HEIGHT),
            "startIndex": 0,
            "endIndex": 0,
            "frameDuration": 1 / 1
        }
        wallpaper = GfxAnimatedSprite(params, 1000, "wallpaper")
        # Add gamepad button input
        startButton = GamepadButton("start", Input.ALL_GAMEPADS_ID, "MENU")
        # Add script to go to next scene
        startScript = SwitchToScene(self, startButton, "SPLASH", "ARCADE", 3)
        # Create Entity + Add all components
        entity = Entity("main")
        entity.addComponent(wallpaper)
        entity.addComponent(startButton)
        entity.addComponent(startScript)
        # Add entity to the scene
        self.addEntity(entity)

    def getTransitionColorOUT(self):
        return (0,0,0)
    def getTransitionTimeOUT(self):
        return 1
    def getTransitionColorIN(self):
        return (0,0,0)
    def getTransitionTimeIN(self):
        return 2


class DisplayRPH(Scene):

    def __init__(self, sceneMgr, sceneName):
        # Init parent class
        super().__init__(sceneMgr, SCREEN_WIDTH, SCREEN_HEIGHT, sceneName)
        # Set debug mode
        self.setDebugMode(False, False, False)
        # Create background image
        params = {
            "filePath": f"resources/images/backgrounds/rphstudio.png",
            "size": (SCREEN_WIDTH, SCREEN_HEIGHT),
            "position": (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            "textureName": f"wallPaper{self.getID()}",
            "spriteBox": (1, 1, SCREEN_WIDTH, SCREEN_HEIGHT),
            "startIndex": 0,
            "endIndex": 0,
            "frameDuration": 1 / 1
        }
        wallpaper = GfxAnimatedSprite(params, 1000, "wallpaper")
        # Add gamepad button input
        startButton = GamepadButton("start", Input.ALL_GAMEPADS_ID, "MENU")
        # Add script to go to next scene
        startScript = SwitchToScene(self, startButton, "SPLASH", "SPLASH", 3)
        # Create Entity + Add all components
        entity = Entity("main")
        entity.addComponent(wallpaper)
        entity.addComponent(startButton)
        entity.addComponent(startScript)
        # Add entity to the scene
        self.addEntity(entity)
    def getTransitionColorOUT(self):
        return (0,0,0)
    def getTransitionTimeOUT(self):
        return 1
    def getTransitionColorIN(self):
        return (0,0,0)
    def getTransitionTimeIN(self):
        return 2


class DisplayArcade(Scene):

    def __init__(self, sceneMgr, sceneName):
        # Init parent class
        super().__init__(sceneMgr, SCREEN_WIDTH, SCREEN_HEIGHT, sceneName)
        # Set debug mode
        self.setDebugMode(False, False, False)
        # Create background image
        params = {
            "filePath": f"resources/images/backgrounds/arcade.png",
            "size": (SCREEN_WIDTH, SCREEN_HEIGHT),
            "position": (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            "textureName": f"wallPaper{self.getID()}",
            "spriteBox": (1, 1, SCREEN_WIDTH, SCREEN_HEIGHT),
            "startIndex": 0,
            "endIndex": 0,
            "frameDuration": 1 / 1
        }
        wallpaper = GfxAnimatedSprite(params, 1000, "wallpaper")
        # Add gamepad button input
        startButton = GamepadButton("start", Input.ALL_GAMEPADS_ID, "MENU")
        # Add script to go to next scene
        startScript = SwitchToScene(self, startButton, "SPLASH", "RPH", 3)
        # Create Entity + Add all components
        entity = Entity("main")
        entity.addComponent(wallpaper)
        entity.addComponent(startButton)
        entity.addComponent(startScript)
        # Add entity to the scene
        self.addEntity(entity)
    def getTransitionColorOUT(self):
        return (0,0,0)
    def getTransitionTimeOUT(self):
        return 1
    def getTransitionColorIN(self):
        return (0,0,0)
    def getTransitionTimeIN(self):
        return 2

