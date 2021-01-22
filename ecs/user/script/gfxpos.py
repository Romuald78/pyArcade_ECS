from ecs.core.components.script import Script


class LimitPosition(Script):

    # CONSTRUCTOR
    def __init__(self, gfx, box, compName=None):
        super().__init__(compName)
        self._gfx = gfx
        self._box = box

    # update
    def updateScript(self, actionName, deltaTime):
        # Get position
        x, y       = self._gfx.getPosition()
        L, R, T, B = self._box
        # check if the gfx component is out of the box
        if x < L:
            x = L
        if x > R:
            x = R
        if y < B:
            y = B
        if y > T:
            y = T
        # update position
        self._gfx.setPosition((x,y))

class Follow(Script):

    # CONSTRUCTOR
    def __init__(self, targetGfx, followerGfx, compName=None):
        super().__init__(compName)
        self._target   = targetGfx
        self._follower = followerGfx

    # update
    def updateScript(self, actionName, deltaTime):
        self._follower.setPosition(self._target.getPosition())


