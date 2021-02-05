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


class SplashScreen(Scene):

    def __init__(self, sceneMgr, sceneName):
        # Init parent class
        super().__init__(sceneMgr, SCREEN_WIDTH, SCREEN_HEIGHT, sceneName)
        # Set debug mode
        self.setDebugMode(False, False, False)
        # init scene
        self.init({})


    def init(self, params):

        # Remove all entities from this scene
        for ent in self.getAllEntities():
            ent.destroy()

        # Set ambient color to dark
        self.setAmbientColor(DARK_LIGHT)

        eFishes  = []
        entFishGen = Entity()
        # Create fish sprite list component
        gfxFishList = GfxAnimSpriteList(ZIDX_FISHES,"FishList")
        entFishGen.addComponent(gfxFishList)

        # Create fish generator
        fishGen = FishGen(self,gfxFishList, eFishes)
        entFishGen.addComponent(fishGen)

        # Store list of registered players. keys are gamepad IDs
        self._players = {}

        # Create parallax Entity
        eParallax = ParallaxFactory().create(SCROLL_SPEED,True)

        # Create background image
        params = {
            "filePath": f"resources/images/backgrounds/sand.png",
            "size": (SCREEN_WIDTH, SCREEN_HEIGHT),
            "position": (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            "textureName": f"splashBG",
            "spriteBox": (1, 1, SCREEN_WIDTH, SCREEN_HEIGHT),
            "startIndex": 0,
            "endIndex": 0,
            "frameDuration": 1 / 1
        }
        wallpaper1 = GfxAnimatedSprite(params, ZIDX_BG-10, "splashBG")
        params = {
            "filePath": f"resources/images/backgrounds/splash_front.png",
            "size": (SCREEN_WIDTH, SCREEN_HEIGHT),
            "position": (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            "textureName": f"splashFG",
            "spriteBox": (1, 1, SCREEN_WIDTH, SCREEN_HEIGHT),
            "startIndex": 0,
            "endIndex": 0,
            "frameDuration": 1 / 1
        }
        wallpaper2 = GfxAnimatedSprite(params, ZIDX_FG, "splashFG")

        # Add gamepad button input
        startButton = GamepadButton("start", Input.ALL_GAMEPADS_ID, "MENU")

        # Add script to go to next scene
        startScript = SwitchToScene(self, startButton, "SELECTION")

        # Create Entity + Add all components
        entity = Entity("main")
        entity.addComponent(wallpaper1)
        entity.addComponent(wallpaper2)
        entity.addComponent(startButton)
        entity.addComponent(startScript)

        # Create lights
        eLights = Entity()
        light1 = LightFx((SCREEN_WIDTH//2, SCREEN_HEIGHT//2), 500, DEFAULT_LIGHT, 'soft')
        moveTorch = MoveTorch(light1,True)
        eLights.addComponent(light1)
        eLights.addComponent(moveTorch)

        # Add entity to the scene
        self.addEntity(entity)
        self.addEntity(entFishGen)
        self.addEntity(eParallax)
        self.addEntity(eLights)



    def getTransitionColorOUT(self):
        return (0,0,0)
    def getTransitionTimeOUT(self):
        return 1
    def getTransitionColorIN(self):
        return (0,0,0)
    def getTransitionTimeIN(self):
        return 2
