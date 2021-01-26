import pymunk

from ecs.core.components.gfx import GfxSimpleSprite
from ecs.core.components.input import GamepadAxis
from ecs.core.components.physic import PhysicBox, PhysicDisc
from ecs.core.main.entity import Entity
from ecs.user.script.phyuserscripts import GfxPhyLink, Move2DAnalogPhy, LimitBoxPhy
from shmup.common.constants import Z_INDEX_SHIPS, SCREEN_HEIGHT, SCREEN_WIDTH, COLLISION_PLAYER_MASK


class InGamePlayerFactory():

    def __init__(self):
        pass

    def create(self, playerInfo):
        # Retrieve player information
        playerName     = playerInfo["name"]
        playerNum      = playerInfo["playerNum"]
        playerCtrlID   = playerInfo["ctrlID"]
        playerColor    = playerInfo["color"]
        playerShipType = playerInfo["shipType"]

        # Create components
        xAxis  = GamepadAxis("moveX", playerCtrlID, "X", 0.2, "xAxis")
        yAxis  = GamepadAxis("moveY", playerCtrlID, "Y", 0.2, "yAxis")
        params = {
            "filePath": f"resources/images/ships/ship01.png",
            "size": (128, 64)
        }
        shipGfx   = GfxSimpleSprite(params, Z_INDEX_SHIPS , "shipGfx")
        params = {
            "mass"         : 0.01,
            "radius"       : 64,
            "mode"         : pymunk.Body.DYNAMIC,
            "pos"          : (500,350+100*playerNum),
            "sensor"       : True,
            "collisionType": COLLISION_PLAYER_MASK | playerNum
        }
        shipPhy    = PhysicDisc(params,"shipPhy")
        gfxPhyLink = GfxPhyLink(shipGfx, shipPhy, "gfxPhyLink")
        moveShip   = Move2DAnalogPhy(shipPhy, xAxis, yAxis, 0.75, "moveShip")
        limitShip  = LimitBoxPhy(shipPhy,(0,SCREEN_HEIGHT),(SCREEN_WIDTH,0),"limitShip")


        # TODO : to be continued...


        # Create antity and add all components to it
        ePlayer = Entity(playerName)
        ePlayer.addComponent(shipGfx)
        ePlayer.addComponent(shipPhy)

        ePlayer.addComponent(xAxis)
        ePlayer.addComponent(yAxis)

        ePlayer.addComponent(moveShip)
        ePlayer.addComponent(gfxPhyLink)
        ePlayer.addComponent(limitShip)

        # return result
        return ePlayer


    def shipsOverlap(self):
        pass
