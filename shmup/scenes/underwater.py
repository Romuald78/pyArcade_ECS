from datetime import datetime
from ecs.core.components.gfx import GfxAnimSpriteList
from ecs.core.components.input import GamepadButton
from ecs.core.main.entity import Entity
from ecs.core.main.scene import Scene
from ecs.user.script.scene import Pause2Buttons
from shmup.common.constants import *
from shmup.factories.parallaxFactory import ParallaxFactory
from shmup.factories.playerFactory import InGamePlayerFactory
from shmup.scripts.fishGen import FishGen


class UnderWater(Scene):

    def _addPauseComponents(self, entity, playerCtrlID):
        # Create components for pause management
        butPause = GamepadButton("PauseGame", playerCtrlID, "MENU", "StartButton")
        butResume = GamepadButton("resumeGame", playerCtrlID, "VIEW", "BackButton")
        scrPause = Pause2Buttons(self, butPause, butResume, "PauseScene")
        butResume.enableOnPause()
        scrPause.enableOnPause()
        # Add these components in the scene management entity
        entity.addComponent(butPause)
        entity.addComponent(butResume)
        entity.addComponent(scrPause)

    def __init__(self, sceneMgr, sceneName):
        # Init parent class
        super().__init__(sceneMgr, SCREEN_WIDTH, SCREEN_HEIGHT, sceneName)
        # Set debug mode
        self.setDebugMode(False, False, False)



    def init(self,params):
        print(f"Init UNDERWATER scene with {params}")

        # create Entity for global scene management
        eManagement = Entity("Management")

        # Create parallax Entity
        eParallax = ParallaxFactory().create()

        # Create fish sprite list component
        gfxFishList = GfxAnimSpriteList(ZIDX_CHARS,"FishList")
        eManagement.addComponent(gfxFishList)

        # Create fish generator
        fishGen = FishGen(self,gfxFishList)
        eManagement.addComponent(fishGen)

        # Create pause components for each gamepad
        for playerName in params:
            # retrieve parameters
            playerInfo   = params[playerName]
            playerCtrlID = playerInfo["ctrlID"]
            # Add pause components
            self._addPauseComponents(eManagement, playerCtrlID)

        # Create entities for all players
        ePlayers = []
        for playerName in params:
            # retrieve parameters
            playerInfo = params[playerName]
            playerCtrlID = playerInfo["ctrlID"]
            # Create player entity (via Factory)and add it to the scene
            ePlayer = InGamePlayerFactory().create(playerInfo)
            # Fill player list
            ePlayers.append(ePlayer)

        # Create spritelist for players
        gfxPlayerSpriteList = GfxAnimSpriteList(ZIDX_CHARS,"sprListPlayers")
        for eP in ePlayers:
            diver  = eP.getComponentsByName("diverGfx")[0]
            shadow = eP.getComponentsByName("shadowGfx")[0]
            gfxPlayerSpriteList.addSprite(shadow)
            gfxPlayerSpriteList.addSprite(diver)
        eManagement.addComponent(gfxPlayerSpriteList)

        # Add ENTITIES to the world
        self.addEntity(eManagement)
        self.addEntity(eParallax)
        for entP in ePlayers:
            self.addEntity(entP)



    def getTransitionColorOUT(self):
        return (0,0,0)
    def getTransitionTimeOUT(self):
        return 1
    def getTransitionColorIN(self):
        return (0,0,0)
    def getTransitionTimeIN(self):
        return 3
