from ecs.core.components.gfx import GfxSimpleSprite, GfxAnimatedSprite, GfxAnimSpriteList
from ecs.core.components.input import GamepadButton, Input
from ecs.core.main.entity import Entity
from ecs.core.main.scene import Scene
from shmup.common.constants import *
from shmup.scripts.fishGen import FishGen
from shmup.scripts.transitions import SwitchToScene


class EndGameScene(Scene):

    def __init__(self, sceneMgr, sceneName):
        # Init parent class
        super().__init__(sceneMgr, SCREEN_WIDTH, SCREEN_HEIGHT, sceneName)
        # Set debug mode
        self.setDebugMode(False, False, False)
        # Add gamepad button input
        startButton = GamepadButton("start", Input.ALL_GAMEPADS_ID, "MENU")
        # Add script to go to next scene
        startScript = SwitchToScene(self, startButton, "SPLASH", "SPLASH", 20)

        # Add backgrounds
        params = {
            "filePath": f"resources/images/backgrounds/endgame.png",
            "size": (SCREEN_WIDTH, SCREEN_HEIGHT),
            "position": (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            "textureName": f"endgame1",
            "spriteBox": (1, 1, SCREEN_WIDTH, SCREEN_HEIGHT),
            "startIndex": 0,
            "endIndex": 0,
            "frameDuration": 1 / 1
        }
        wallpaper1 = GfxAnimatedSprite(params, ZIDX_BG, "wallpaper")
        params = {
            "filePath": f"resources/images/backgrounds/gameover.png",
            "size": (SCREEN_WIDTH, SCREEN_HEIGHT),
            "position": (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            "textureName": f"endgame2",
            "spriteBox": (1, 1, SCREEN_WIDTH, SCREEN_HEIGHT),
            "startIndex": 0,
            "endIndex": 0,
            "frameDuration": 1 / 1
        }
        wallpaper2 = GfxAnimatedSprite(params, ZIDX_HUD, "gmovr")

        # Create fish generator
        eFishes = []
        gfxFishList = GfxAnimSpriteList(ZIDX_FISHES, "FishList")
        fishGen = FishGen(self,gfxFishList, eFishes)

        # Create Entity + Add all components
        entity = Entity("main")
        entity.addComponent(startButton)
        entity.addComponent(startScript)
        entity.addComponent(wallpaper1)
        entity.addComponent(wallpaper2)
        entity.addComponent(gfxFishList)
        entity.addComponent(fishGen)


        # Add entity to the scene
        self.addEntity(entity)

    def getTransitionColorOUT(self):
        return (0,0,0)
    def getTransitionTimeOUT(self):
        return 1
    def getTransitionColorIN(self):
        return (255,0,0)
    def getTransitionTimeIN(self):
        return 1.5
