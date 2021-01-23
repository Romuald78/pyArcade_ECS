import arcade

from ecs.core.components.input import Keyboard, GamepadButton
from ecs.core.main.entity import Entity
from ecs.core.main.scene import Scene
from ecs.user.script.scene import PauseToggle, Pause2Buttons
from shmup.common.constants import *
from shmup.factories.player import InGamePlayerFactory
from shmup.scripts.collisions import PlayerCollision


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
        eManagement = Entity("Management")
        eCollisions = Entity("Collisions")

        # Create entities for all players
        ePlayers = []
        for playerName in params:
            # retrieve parameters
            playerInfo = params[playerName]
            playerCtrlID   = playerInfo["ctrlID"]

            # Add pause components
            self._addPauseComponents(eManagement, playerCtrlID)

            # Create player entity (via Factory)and add it to the scene
            ePlayer = self.playerFactory.create(playerInfo)
            self.addEntity(ePlayer)

            # Fill player list
            ePlayers.append(ePlayer)

        # If there are at least two players
        # create collisions
        if len(ePlayers) > 1:
            gfx1    = ePlayers[0].getComponentsByName("ShipGfx")[0]
            gfx2    = ePlayers[1].getComponentsByName("ShipGfx")[0]
            collide = PlayerCollision(gfx1, gfx2, 128, 64, eCollisions, "Collide")
            eManagement.addComponent(collide)
            pass

        # Add collisions entity
        self.addEntity(eCollisions)

        # Add Management entity in the scene
        self.addEntity(eManagement)


