import pymunk

from ecs.core.components.gfx import GfxSimpleSprite, GfxAnimatedSprite, GfxText
from ecs.core.components.input import GamepadAxis
from ecs.core.components.physic import PhysicBox, PhysicDisc
from ecs.core.main.entity import Entity
from ecs.user.idle.counters import UserCounter
from ecs.user.script.gfxpos import Follow
from ecs.user.script.phyuserscripts import GfxPhyLink, Move2DAnalogPhy, LimitBoxPhy
from shmup.common.constants import Z_INDEX_SHIPS, SCREEN_HEIGHT, SCREEN_WIDTH, COLLISION_PLAYER_MASK, ZIDX_DIVERS, \
    COLL_TYPE_DIVER


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


        # -----------------------------
        # IDLE Components
        # -----------------------------
        # Player life
        life = UserCounter(0,100,100,True,"diverLife")


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
        params = {
            "x": 500,
            "y": 500,
            "message": str(life.getValue()),
            "size":50
        }
        textGfx = GfxText(params,0,"lifeText")


        # -----------------------------
        # PHYSIC Components
        # -----------------------------
        params = {
            "mass"         : 0.01,
            "radius"       : 64,
            "mode"         : pymunk.Body.DYNAMIC,
            "pos"          : (500,350+100*playerNum),
            "sensor"       : False,
            "collisionType": COLL_TYPE_DIVER,
        }
        diverPhy   = PhysicDisc(params,"diverPhy")


        # -----------------------------
        # Scripts components
        # -----------------------------
        # shadow follows diver
        follow     = Follow(diverGfx, shadowGfx, "followDiver")
        follow2    = Follow(diverGfx, textGfx, "followDiver")
        # diver is linked to physic
        gfxPhyLink = GfxPhyLink(diverGfx, diverPhy, "gfxPhyLink")
        # physic comp is moved by gamepad
        moveDiver  = Move2DAnalogPhy(diverPhy, xAxis, yAxis, 1, "moveDiver")
        # physic stays on Screen
        limitDiver = LimitBoxPhy(diverPhy,(0,SCREEN_HEIGHT),(SCREEN_WIDTH,0),"limitDiver")

        # Create antity and add all components to it
        ePlayer = Entity(playerName)
        ePlayer.addComponent(xAxis)
        ePlayer.addComponent(yAxis)
        ePlayer.addComponent(diverGfx)
        ePlayer.addComponent(shadowGfx)
        ePlayer.addComponent(textGfx)
        ePlayer.addComponent(diverPhy)
        ePlayer.addComponent(moveDiver)
        ePlayer.addComponent(gfxPhyLink)
        ePlayer.addComponent(limitDiver)
        ePlayer.addComponent(follow)
        ePlayer.addComponent(follow2)
        ePlayer.addComponent(life)

        # return result
        return ePlayer
