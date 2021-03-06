from ecs.core.components.gfx import GfxSimpleSprite, GfxAnimatedSprite, GfxAnimSpriteList
from ecs.core.components.input import GamepadButton, Input
from ecs.core.components.light import LightFx
from ecs.core.main.entity import Entity
from ecs.core.main.scene import Scene
from shmup.common.constants import *
from shmup.factories.parallaxFactory import ParallaxFactory
from shmup.scripts.fishGen import FishGen
from shmup.scripts.moveTorch import MoveTorch
from shmup.scripts.transitions import SwitchToScene


class EndGameScene(Scene):

    def __init__(self, sceneMgr, sceneName):
        # Init parent class
        super().__init__(sceneMgr, SCREEN_WIDTH, SCREEN_HEIGHT, sceneName)
        # Set debug mode
        self.setDebugMode(False, False, False)
        self.init({})


    def init(self, params):
        # Remove all entities from this scene
        for ent in self.getAllEntities():
            ent.destroy()

        # Dark light
        self.setAmbientColor(DARK_LIGHT)

        # Add gamepad button input
        startButton = GamepadButton("start", Input.ALL_GAMEPADS_ID, "MENU")
        # Add script to go to next scene
        startScript = SwitchToScene(self, startButton, "SPLASH", "SPLASH", 60)

        # Create parallax Entity
        eParallax = ParallaxFactory().create(SCROLL_SPEED,True)

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
        wallpaper1 = GfxAnimatedSprite(params, ZIDX_BG-50, "wallpaper")
        params = {
            "filePath": f"resources/images/backgrounds/endgame_front.png",
            "size": (SCREEN_WIDTH, SCREEN_HEIGHT),
            "position": (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            "textureName": f"endgameFrnt",
            "spriteBox": (1, 1, SCREEN_WIDTH, SCREEN_HEIGHT),
            "startIndex": 0,
            "endIndex": 0,
            "frameDuration": 1 / 1
        }
        wallpaper2 = GfxAnimatedSprite(params, ZIDX_FG, "wallpaper")
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
        wallpaper3 = GfxAnimatedSprite(params, ZIDX_HUD, "gmovr")

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
        entity.addComponent(wallpaper3)
        entity.addComponent(gfxFishList)
        entity.addComponent(fishGen)

        # Create lights
        eLights = Entity()
        light1 = LightFx((SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 500, DEFAULT_LIGHT, 'soft')
        moveTorch = MoveTorch(light1)
        eLights.addComponent(light1)
        eLights.addComponent(moveTorch)

        # Add entity to the scene
        self.addEntity(entity)
        self.addEntity(eParallax)
        self.addEntity(eLights)

    def getTransitionColorOUT(self):
        return (0,0,0)
    def getTransitionTimeOUT(self):
        return 1
    def getTransitionColorIN(self):
        return (255,0,0)
    def getTransitionTimeIN(self):
        return 1.5
