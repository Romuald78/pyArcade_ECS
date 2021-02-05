import pymunk

from ecs.core.components.gfx import GfxSimpleSprite, GfxAnimatedSprite, GfxText
from ecs.core.components.input import GamepadAxis, GamepadButton
from ecs.core.components.light import LightFx
from ecs.core.components.physic import PhysicBox, PhysicDisc
from ecs.core.main.entity import Entity
from ecs.user.idle.counters import UserCounter
from ecs.user.script.gfxpos import Follow, LightFollowGfx
from ecs.user.script.phyuserscripts import GfxPhyLink, Move2DAnalogPhy, LimitBoxPhy
from shmup.common.constants import Z_INDEX_SHIPS, SCREEN_HEIGHT, SCREEN_WIDTH, COLLISION_PLAYER_MASK, ZIDX_DIVERS, \
    COLL_TYPE_DIVER, DEFAULT_LIGHT
from shmup.factories.bubbleFactory import BubbleFactory
from shmup.scripts.genBubble import GenBubble


class InGamePlayerFactory():

    def __init__(self):
        pass

    def create(self, playerInfo):
        # Retrieve player information
        playerName     = playerInfo["name"]
        playerNum      = playerInfo["playerNum"]
        playerCtrlID   = playerInfo["ctrlID"]
        playerColor    = playerInfo["color"]

        # -----------------------------
        # INPUT Components
        # -----------------------------
        xAxis  = GamepadAxis("moveX", playerCtrlID, "X", 0.1, "xAxis")
        yAxis  = GamepadAxis("moveY", playerCtrlID, "Y", 0.1, "yAxis")
        buttA  = GamepadButton("FIRE", playerCtrlID, "A", "buttA")

        # -----------------------------
        # IDLE Components
        # -----------------------------
        # Player life
        life = UserCounter(0,21,21,True,"diverLife")
        # Player score
        score = UserCounter(0, 100000, 0, True, "diverScore")


        # -----------------------------
        # GFX Components
        # -----------------------------
        params = {
            "filePath": f"resources/images/divers/diver01.png",
            "spriteBox": (4, 4, 150, 100),
            "startIndex": 0,
            "endIndex": 7,
            "frameDuration": 1 / 24,
            "size": (300, 200),
            "textureName": f"diver{playerNum}"
        }
        diverGfx = GfxAnimatedSprite(params, ZIDX_DIVERS, "diverGfx")
        params = {
            "filePath": f"resources/images/divers/diver02.png",
            "spriteBox": (4, 4, 150, 100),
            "startIndex": 0,
            "endIndex": 7,
            "frameDuration": 1 / 24,
            "size": (300, 200),
            "filterColor": playerColor,
            "textureName": f"shadow{playerNum}"
        }
        shadowGfx = GfxAnimatedSprite(params, ZIDX_DIVERS, "shadowGfx")
#        params = {
#            "x": 500,
#            "y": 500,
#            "message": str(life.getValue()),
#            "size":50
#        }
#        textGfx = GfxText(params,0,"lifeText")


        # -----------------------------
        # PHYSIC Components
        # -----------------------------
        params = {
            "mass"         : 0.01,
            "radius"       : 64,
            "mode"         : pymunk.Body.KINEMATIC,
            "pos"          : (500,350+100*playerNum),
            "sensor"       : True,
            "collisionType": COLL_TYPE_DIVER,
        }
        diverPhy   = PhysicDisc(params,"diverPhy")



        # -----------------------------
        # Scripts components
        # -----------------------------
        # shadow follows diver
        follow     = Follow(diverGfx, shadowGfx, "followDiver")
#        follow2    = Follow(diverGfx, textGfx, "followDiver")
        # diver is linked to physic
        offset = (-64,0)
        gfxPhyLink = GfxPhyLink(diverGfx, diverPhy, offset, "gfxPhyLink")
        # physic comp is moved by gamepad
        moveDiver  = Move2DAnalogPhy(diverPhy, xAxis, yAxis, 20, "moveDiver")
        # physic stays on Screen
        dx = 150+offset[0]
        dy = 120+offset[1]
        limitDiver = LimitBoxPhy(diverPhy,(dx,SCREEN_HEIGHT-dy+40),(SCREEN_WIDTH-dx,dy),"limitDiver")

        # light
        light = LightFx((-1000,-1000),160,playerColor,"soft")
        lightFollow = LightFollowGfx(diverGfx, light)

        # Create antity and add all components to it
        ePlayer = Entity(playerName)
        ePlayer.addComponent(xAxis)
        ePlayer.addComponent(yAxis)
        ePlayer.addComponent(buttA)
        ePlayer.addComponent(diverGfx)
        ePlayer.addComponent(shadowGfx)
        ePlayer.addComponent(diverPhy)
        ePlayer.addComponent(moveDiver)
        ePlayer.addComponent(gfxPhyLink)
        ePlayer.addComponent(limitDiver)
        ePlayer.addComponent(follow)
        ePlayer.addComponent(life)
        ePlayer.addComponent(score)
        ePlayer.addComponent(light)
        ePlayer.addComponent(lightFollow)


        # return result
        return ePlayer
