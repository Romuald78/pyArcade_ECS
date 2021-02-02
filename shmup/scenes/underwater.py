from ecs.core.components.gfx import GfxAnimSpriteList
from ecs.core.components.input import GamepadButton
from ecs.core.main.entity import Entity
from ecs.core.main.scene import Scene
from ecs.user.script.scene import Pause2Buttons
from shmup.common.constants import *
from shmup.factories.bubbleFactory import BubbleFactory
from shmup.factories.hudFactory import HudFactory
from shmup.factories.parallaxFactory import ParallaxFactory
from shmup.factories.playerFactory import InGamePlayerFactory
from shmup.scripts.collisions import FishCollisions, BubbleCollisions
from shmup.scripts.destroyPlayer import DestroyPlayer
from shmup.scripts.endgamescr import EndGameScr
from shmup.scripts.fishGen import FishGen
from shmup.scripts.genBubble import GenBubble


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

        # Remove all entities from this scene
        for ent in self.getAllEntities():
            ent.destroy()

        # create Entity for global scene management
        eManagement = Entity("Management")

        # Lists of entities
        ePlayers = []
        eFishes  = []
        eBubbles = []
        eHUDs    = []

        # Create fish sprite list component
        gfxFishList = GfxAnimSpriteList(ZIDX_FISHES,"FishList")
        eManagement.addComponent(gfxFishList)

        # Create fish generator
        fishGen = FishGen(self,gfxFishList, eFishes)
        eManagement.addComponent(fishGen)

        # Create pause components for each gamepad
        for playerName in params:
            # retrieve parameters
            playerInfo   = params[playerName]
            playerCtrlID = playerInfo["ctrlID"]
            # Add pause components
            self._addPauseComponents(eManagement, playerCtrlID)

        # Create entities for all players and HUD
        for playerName in params:
            # retrieve parameters
            playerInfo = params[playerName]
            playerCtrlID = playerInfo["ctrlID"]
            # Create player entity (via Factory)and add it to the scene
            ePlayer = InGamePlayerFactory().create(playerInfo)
            # Fill player list
            ePlayers.append(ePlayer)
            # Create hud
            life = ePlayer.getComponentsByName("diverLife")[0]
            scr  = ePlayer.getComponentsByName("diverScore")[0]
            eHud = HudFactory().create(playerInfo["playerNum"], playerInfo["color"], life, scr)
            eHUDs.append(eHud)

        # Create spritelist for players
        gfxPlayerSpriteList = GfxAnimSpriteList(ZIDX_DIVERS,"sprListPlayers")
        for eP in ePlayers:
            diver  = eP.getComponentsByName("diverGfx")[0]
            shadow = eP.getComponentsByName("shadowGfx")[0]
            gfxPlayerSpriteList.addSprite(shadow)
            gfxPlayerSpriteList.addSprite(diver)
        eManagement.addComponent(gfxPlayerSpriteList)

        # Create collision management
        collide1 = FishCollisions(eManagement, COLL_TYPE_DIVER, COLL_TYPE_FISH, ePlayers)
        eManagement.addComponent(collide1)
        collide2 = BubbleCollisions(eManagement, COLL_TYPE_FISH, COLL_TYPE_BUBBLE, eFishes, eBubbles)
        eManagement.addComponent(collide2)

        # Create parallax Entity
        eParallax = ParallaxFactory().create(SCROLL_SPEED2)

        # Create bubble generation
        gfxBubbleSpriteList = GfxAnimSpriteList(ZIDX_BUBBLES,"sprListBubbles")
        for eP in ePlayers:
            diver  = eP.getComponentsByName("diverGfx")[0]
            buttA  = eP.getComponentsByName("buttA")[0]
            score  = eP.getComponentsByName("diverScore")[0]
            genBub = GenBubble(self, diver, buttA, gfxBubbleSpriteList, eBubbles , {"score":score}, "genBub")
            eManagement.addComponent(genBub)
        eManagement.addComponent(gfxBubbleSpriteList)

        # Create player destroy
        for eP in ePlayers:
            lf = eP.getComponentsByName("diverLife")[0]
            dstry = DestroyPlayer(lf, eP)
            eManagement.addComponent(dstry)

        # Create END game condition
        endScr = EndGameScr(ePlayers)
        eManagement.addComponent(endScr)


        # Add ENTITIES to the world
        self.addEntity(eManagement)
        self.addEntity(eParallax)
        for entP in ePlayers:
            self.addEntity(entP)
        for entH in eHUDs:
            self.addEntity(entH)



    def getTransitionColorOUT(self):
        return (255,0,0)
    def getTransitionTimeOUT(self):
        return 1.5
    def getTransitionColorIN(self):
        return (0,0,0)
    def getTransitionTimeIN(self):
        return 3
