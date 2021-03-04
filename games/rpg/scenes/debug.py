from random import randint

import arcade

from ecs.core.components.camera import Camera
from ecs.core.components.input import Keyboard
from ecs.core.main.entity import Entity
from ecs.core.main.scene import Scene
from ecs.user.script.follow import CameraFollowTransform
from ecs.user.script.cameras import ZoomCamera, SwitchCameras
from games.rpg.factories.PlayerFactory import PlayerFactory
from games.rpg.factories.SkeletonFactory import SkeletonFactory
from games.rpg.factories.TreeFactory import TreeFactory
from shmup.common.constants import *


class RpgDebug(Scene):

    def __init__(self, sceneMgr, sceneName):
        # Init parent class
        super().__init__(sceneMgr, SCREEN_WIDTH//2, SCREEN_HEIGHT//2, sceneName)
        # Set debug mode
        self.setDebugMode(False, False, False)

    def init(self, params):


        # -----------------------------
        # Player
        # -----------------------------
        # Create entity
        player = PlayerFactory().create()
        # Add entity to the scene
        self.addEntity(player)


        # -----------------------------
        # Camera
        # -----------------------------
        # create camera list
        camList = []
        # Create entity
        camEntity = Entity()
        # Add camera
        camera = Camera( (SCREEN_WIDTH//2, SCREEN_HEIGHT//2), (SCREEN_WIDTH/3, SCREEN_HEIGHT/3))
        camList.append(camera)
        # Add script to follow player transform
        pTrans = player.getFirstComponentByName("transform")
        camFollow = CameraFollowTransform(camera, pTrans, 20, 150, "log")
        camEntity.addComponent(camera)
        camEntity.addComponent(camFollow)
        # Add keys and script to zoom IN/OUT
        keyP = Keyboard("zoomPlus" , arcade.key.NUM_ADD     )
        keyM = Keyboard("zoomMinus", arcade.key.NUM_SUBTRACT)
        zoomScr = ZoomCamera(camera, keyP, keyM)
        # Add components to entity
        camEntity.addComponent(keyP)
        camEntity.addComponent(keyM)
        camEntity.addComponent(zoomScr)

        # Add 2nd camera for global zone
        cameraMain = Camera((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (SCREEN_WIDTH, SCREEN_HEIGHT))
        camList.append(cameraMain)
        # Add keys to select cams
        keyNext = Keyboard("nextCam", arcade.key.PAGEDOWN)
        keyPrev = Keyboard("prevCam", arcade.key.PAGEUP  )
        # Add script to switch between player camera and global camera
        switchCams = SwitchCameras(self, camList, keyNext, keyPrev)
        # Add components to entity
        camEntity.addComponent(cameraMain)
        camEntity.addComponent(keyNext)
        camEntity.addComponent(keyPrev)
        camEntity.addComponent(switchCams)

        # Add entity to the scene
        self.addEntity(camEntity)




        # -----------------------------
        # Enemies
        # -----------------------------
        for i in range(20):
            randPos = (randint(50, SCREEN_WIDTH - 50), randint(50, SCREEN_HEIGHT - 50))
            # Create entity
            skel = SkeletonFactory().create( randPos )
            # Add entity to the scene
            self.addEntity(skel)
            # Get moveAI component and player physic component
            moveAI    = skel.getFirstComponentByName("moveAI")
            playerPhy = player.getFirstComponentByName("phy")
            moveAI.setTarget(playerPhy)

        # -----------------------------
        # Trees
        # -----------------------------
        # Create several trees
        for i in range(20):
            # Create entity
            tree = TreeFactory().create(( randint(74,SCREEN_WIDTH-74), randint(10,SCREEN_HEIGHT-138) ))
            # Add entity to the scene
            self.addEntity(tree)




