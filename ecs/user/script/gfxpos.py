import math

from ecs.core.components.script import Script


class LimitBox(Script):

    # CONSTRUCTOR
    def __init__(self, gfx, topLeftPos, bottomRightPos, compName=None):
        super().__init__(compName)
        self._gfx = gfx
        self._L = topLeftPos[0]
        self._T = topLeftPos[1]
        self._R = bottomRightPos[0]
        self._B = bottomRightPos[1]

    # update
    def updateScript(self, actionName, deltaTime):
        # Get position
        x, y       = self._gfx.getPosition()
        # check if the gfx component is out of the box
        if x < self._L:
            x = self._L
        if x > self._R:
            x = self._R
        if y < self._B:
            y = self._B
        if y > self._T:
            y = self._T
        # update position
        self._gfx.setPosition((x,y))

class LimitCircle(Script):

    # CONSTRUCTOR
    def __init__(self, gfx, center, radius, compName=None):
        super().__init__(compName)
        self._gfx = gfx
        self._xc  = center[0]
        self._yc  = center[1]
        self._r   = radius

    # update
    def updateScript(self, actionName, deltaTime):
        # Get position
        x, y = self._gfx.getPosition()
        dx = x - self._xc
        dy = y - self._yc
        dist2 = dx*dx+dy*dy
        # if too far
        if dist2 > self._r*self._r:
            # compute angle
            ang   = math.atan2(dy,dx)
            newDx = math.cos(ang) * self._r
            newDy = math.sin(ang) * self._r
            self._gfx.setPosition((self._xc+newDx, self._yc+newDy))

class Follow(Script):

    # CONSTRUCTOR
    def __init__(self, targetGfx, followerGfx, compName=None):
        super().__init__(compName)
        self._target   = targetGfx
        self._follower = followerGfx

    # update
    def updateScript(self, actionName, deltaTime):
        self._follower.setPosition(self._target.getPosition())


