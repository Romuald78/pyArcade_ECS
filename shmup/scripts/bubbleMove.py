import math

from ecs.core.components.script import Script


class BubbleMove(Script):


    def __init__(self, phy, compName=None):
        super().__init__(compName)
        self._phy = phy
        self._initialImpulse = False

    def updateScript(self, scriptName, deltaTime):
        self._phy.setAngle(0)
        if not self._initialImpulse:
            self._initialImpulse = True
            dx = 30
            self._phy.applyForce(dx, 0)
        else:
            dy = 0.5
            self._phy.applyForce(0, dy)

