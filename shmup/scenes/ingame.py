import arcade

from ecs.core.components.input import Keyboard, GamepadButton
from ecs.core.main.entity import Entity
from ecs.core.main.scene import Scene
from ecs.user.script.scene import PauseToggle, Pause2Buttons
from shmup.common.constants import *
from shmup.factories.player import InGamePlayerFactory
from shmup.scripts.collisions import PlayerCollision
from shmup.scripts.fox import Fox


class InGame(Scene):

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
        self.setDebugMode(False, True)
        # Player factory
        self.playerFactory = InGamePlayerFactory()


    def init(self,params):
        print(f"Init IN-GAME scene with {params}")

        # create Entity for global scene management
        eManagement    = Entity("Management")
        eCollideBursts = Entity("CollideBursts")

        # Create entities for all players
        ePlayers = []
        for playerName in params:
            # retrieve parameters
            playerInfo   = params[playerName]
            playerCtrlID = playerInfo["ctrlID"]

            # Add pause components
            self._addPauseComponents(eManagement, playerCtrlID)

            # Create player entity (via Factory)and add it to the scene
            ePlayer = self.playerFactory.create(playerInfo)
            self.addEntity(ePlayer)

            # Fill player list
            ePlayers.append(ePlayer)

        # If there are at least two players
        # create collisions
        for i in range(len(ePlayers)):
            for j in range(i+1,len(ePlayers)):
                gfx1   = ePlayers[i].getComponentsByName("shipGfx")[0]
                gfx2   = ePlayers[j].getComponentsByName("shipGfx")[0]
                phy1   = ePlayers[i].getComponentsByName("shipPhy")[0]
                phy2   = ePlayers[j].getComponentsByName("shipPhy")[0]
                print(f"Add {gfx1} {gfx2}")
                colTyp1 = phy1.getCollisionType()
                colTyp2 = phy2.getCollisionType()
                fox    = None
                # Create Fox component
                if i==0 and j==0:
                    fox = Fox(gfx1,"FoxRules")
                    eManagement.addComponent(fox)
                # Create all collisions
                collide = PlayerCollision(self.getPhysicWorld(), fox, gfx1, gfx2, colTyp1, colTyp2, eCollideBursts, f"Collide{i}{j}")
                eManagement.addComponent(collide)


        # Add collisions entity
        self.addEntity(eCollideBursts)

        # Add Management entity in the scene
        self.addEntity(eManagement)


