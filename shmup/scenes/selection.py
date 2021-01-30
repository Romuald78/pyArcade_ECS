from ecs.core.components.gfx import GfxSimpleSprite, GfxAnimatedSprite, GfxAnimSpriteList
from ecs.core.components.input import GamepadButton, Input
from ecs.core.main.entity import Entity
from ecs.core.main.scene import Scene
from shmup.common.constants import *
from shmup.factories.parallaxFactory import ParallaxFactory
from shmup.scripts.fishGen import FishGen
from shmup.scripts.playerSelect import PlayerSelection
from shmup.scripts.transitions import SwitchToScene


class Selection(Scene):

    def __init__(self, sceneMgr, sceneName):
        # Init parent class
        super().__init__(sceneMgr, SCREEN_WIDTH, SCREEN_HEIGHT, sceneName)
        # Set debug mode
        self.setDebugMode(False, False, False)

    def init(self, params):

        # Remove all entities from this scene
        for ent in self.getAllEntities():
            ent.destroy()

        # init player list
        self.players = {}

        eFishes  = []
        entFishGen = Entity()
        # Create fish sprite list component
        gfxFishList = GfxAnimSpriteList(ZIDX_FISHES,"FishList")
        entFishGen.addComponent(gfxFishList)

        # Create fish generator
        fishGen = FishGen(self,gfxFishList, eFishes)
        entFishGen.addComponent(fishGen)


        # Create parallax Entity
        eParallax = ParallaxFactory().create(-5,True)

        # Create background image
        params = {
            "filePath": f"resources/images/backgrounds/sand.png",
            "size": (SCREEN_WIDTH, SCREEN_HEIGHT),
            "position": (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            "textureName": f"selectBG",
            "spriteBox": (1, 1, SCREEN_WIDTH, SCREEN_HEIGHT),
            "startIndex": 0,
            "endIndex": 0,
            "frameDuration": 1 / 1
        }
        wallpaper1 = GfxAnimatedSprite(params, ZIDX_BG-10, "splashBG")


        # Create background image
        params = {
            "filePath": f"resources/images/backgrounds/playerSelection.png",
            "size": (SCREEN_WIDTH, SCREEN_HEIGHT),
            "position": (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
            "textureName": f"selectFG",
            "spriteBox": (1, 1, SCREEN_WIDTH, SCREEN_HEIGHT),
            "startIndex": 0,
            "endIndex": 0,
            "frameDuration": 1 / 1
        }
        wallpaper = GfxAnimatedSprite(params, ZIDX_FG, "wallpaper")

        # Add gamepad button input
        backButton  = GamepadButton("back",  Input.ALL_GAMEPADS_ID, "VIEW")
        startButton = GamepadButton("start", Input.ALL_GAMEPADS_ID, "MENU")

        # Add script to (un)register players
        register = PlayerSelection(self.players, startButton, backButton, self, "SPLASH", "UNDERWATER")

        # Create Entity + Add all components
        entity = Entity("main")
        entity.addComponent(wallpaper1)
        entity.addComponent(wallpaper)
        entity.addComponent(startButton)
        entity.addComponent(backButton)
        entity.addComponent(register)

        # Add entity to the scene
        self.addEntity(entity)
        self.addEntity(eParallax)
        self.addEntity(entFishGen)

    def getTransitionColorIN(self):
        return (0,0,0)
    def getTransitionTimeIN(self):
        return 2
    def getTransitionColorOUT(self):
        return (0,0,0)
    def getTransitionTimeOUT(self):
        return 1
