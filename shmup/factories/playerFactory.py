import pymunk

from ecs.core.components.gfx import GfxSimpleSprite, GfxAnimatedSprite
from ecs.core.components.input import GamepadAxis
from ecs.core.components.physic import PhysicBox, PhysicDisc
from ecs.core.main.entity import Entity
from ecs.user.script.gfxpos import Follow
from ecs.user.script.phyuserscripts import GfxPhyLink, Move2DAnalogPhy, LimitBoxPhy
from shmup.common.constants import Z_INDEX_SHIPS, SCREEN_HEIGHT, SCREEN_WIDTH, COLLISION_PLAYER_MASK, ZIDX_CHARS


class InGamePlayerFactory():

    def __init__(self):
        pass

    def create(self, playerInfo):
        # Retrieve player information
        playerName     = playerInfo["name"]
        playerNum      = playerInfo["playerNum"]
        playerCtrlID   = playerInfo["ctrlID"]
        playerColor    = playerInfo["color"]

        # Create components
        xAxis  = GamepadAxis("moveX", playerCtrlID, "X", 0.1, "xAxis")
        yAxis  = GamepadAxis("moveY", playerCtrlID, "Y", 0.1, "yAxis")
        params = {
            "filePath": f"resources/images/divers/diver01.png",
            "spriteBox": (4, 4, 150, 100),
            "startIndex": 0,
            "endIndex": 7,
            "frameDuration": 1 / 24,
            "size": (300, 200),
            "textureName": f"diver{playerNum}"
        }
        diverGfx = GfxAnimatedSprite(params, ZIDX_CHARS, "diverGfx")
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
        shadowGfx = GfxAnimatedSprite(params, ZIDX_CHARS, "shadowGfx")
        params = {
            "mass"         : 0.01,
            "radius"       : 64,
            "mode"         : pymunk.Body.DYNAMIC,
            "pos"          : (500,350+100*playerNum),
            "sensor"       : False,
            "collisionType": COLLISION_PLAYER_MASK | playerNum,
        }
        follow     = Follow(diverGfx, shadowGfx, "followDiver")
        diverPhy   = PhysicDisc(params,"diverPhy")
        gfxPhyLink = GfxPhyLink(diverGfx, diverPhy, "gfxPhyLink")
        moveDiver  = Move2DAnalogPhy(diverPhy, xAxis, yAxis, 1, "moveDiver")
        limitDiver = LimitBoxPhy(diverPhy,(0,SCREEN_HEIGHT),(SCREEN_WIDTH,0),"limitDiver")

        # Create antity and add all components to it
        ePlayer = Entity(playerName)
        ePlayer.addComponent(diverGfx)
        ePlayer.addComponent(shadowGfx)
        ePlayer.addComponent(diverPhy)
        ePlayer.addComponent(xAxis)
        ePlayer.addComponent(yAxis)
        ePlayer.addComponent(moveDiver)
        ePlayer.addComponent(gfxPhyLink)
        ePlayer.addComponent(limitDiver)
        ePlayer.addComponent(follow)

        # return result
        return ePlayer
