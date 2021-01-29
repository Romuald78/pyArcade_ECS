import math

from ecs.core.components.script import Script


class GfxPhyLink(Script):

    # CONSTRUCTOR
    def __init__(self, gfx, phy, offset, compName=None):
        super().__init__(compName)
        self._gfx = gfx
        self._phy = phy
        self._offset = offset

    # update
    def updateScript(self, actionName, deltaTime):
        # copy position
        phyPos = self._phy.getPosition()
        newPos = (phyPos[0]+self._offset[0], phyPos[1]+self._offset[1])
        self._gfx.setPosition(newPos)
        # copy angle
        phyAng = self._phy.getAngle()
        self._gfx.setAngle(phyAng*180/math.pi)

class PhyGfxLink(Script):

    # CONSTRUCTOR
    def __init__(self, phy, gfx, offset, compName=None):
        super().__init__(compName)
        self._gfx = gfx
        self._phy = phy
        self._offset = offset

    # update
    def updateScript(self, actionName, deltaTime):
        # copy position
        gfxPos = self._gfx.getPosition()
        newPos = (gfxPos[0]+self._offset[0],gfxPos[1]+self._offset[1])
        self._phy.setPosition(newPos)
        # copy angle
        gfxAng = self._gfx.getAngle()
        self._phy.setAngle(gfxAng*math.pi/180)



class Move2DAnalogPhy(Script):

    # constructor
    def __init__(self, phy, xAxis, yAxis, speed, compName=None):
        super().__init__(compName)
        self._phy   = phy
        self._xAxis = xAxis
        self._yAxis = yAxis
        self._speed = speed

    # update
    def updateScript(self, actionName, deltaTime):
        dx =  self._xAxis.getValue()*self._speed
        dy = -self._yAxis.getValue()*self._speed
        self._phy.applyImpulse(dx, dy)
        # Force angle to 0
        self._phy.setAngle(0)


class LimitBoxPhy(Script):

    # CONSTRUCTOR
    def __init__(self, phy, topLeftPos, bottomRightPos, compName=None):
        super().__init__(compName)
        self._phy = phy
        self._L = topLeftPos[0]
        self._T = topLeftPos[1]
        self._R = bottomRightPos[0]
        self._B = bottomRightPos[1]

    # update
    def updateScript(self, actionName, deltaTime):
        # Get position
        x, y   = self._phy.getPosition()
        dx, dy = self._phy.getVelocity()
        # check if the gfx component is out of the box
        limit = False
        if x < self._L:
            limit = True
            x = self._L
            dx = 0
        if x > self._R:
            limit = True
            x = self._R
            dx = 0
        if y < self._B:
            limit = True
            y = self._B
            dy = 0
        if y > self._T:
            limit = True
            y = self._T
            dy = 0

        # update position
        if limit:
            self._phy.setPosition((x,y))
            self._phy.setVelocity((dx,dy))


