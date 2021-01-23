from ecs.core.components.gfx import GfxSimpleSprite
from ecs.core.components.input import GamepadAxis
from ecs.core.main.entity import Entity
from ecs.user.script.gfxpos import Move2DAnalog, LimitBox
from shmup.common.constants import Z_INDEX_SHIPS, SCREEN_HEIGHT, SCREEN_WIDTH


class InGamePlayerFactory():

    def __init__(self):
        pass

    def create(self, playerInfo):
        # Retrieve player information
        playerName     = playerInfo["name"]
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
        shipGfx   = GfxSimpleSprite(self, params, Z_INDEX_SHIPS , "ShipGfx")
        moveShip  = Move2DAnalog(shipGfx, xAxis, yAxis, 12, "moveShip")
        limitShip = LimitBox(shipGfx,(0,SCREEN_HEIGHT),(SCREEN_WIDTH,0),"limitShip")

        # TODO : to be continued...

        # Create antity and add all components to it
        ePlayer = Entity(playerName)
        ePlayer.addComponent(shipGfx)
        ePlayer.addComponent(xAxis)
        ePlayer.addComponent(yAxis)
        ePlayer.addComponent(moveShip)
        ePlayer.addComponent(limitShip)

        # return result
        return ePlayer

