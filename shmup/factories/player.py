from ecs.core.components.input import GamepadAxis
from ecs.core.main.entity import Entity


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
        xAxis = GamepadAxis("moveX", playerCtrlID, "X")
        yAxis = GamepadAxis("moveY", playerCtrlID, "Y")

        # TODO : to be continued...

        # Create antity and add all components to it
        ePlayer = Entity(playerName)
        ePlayer.addComponent(xAxis)
        ePlayer.addComponent(yAxis)

        # return result
        return ePlayer

