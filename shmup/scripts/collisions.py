from ecs.core.components.gfx import GfxBurstEmitter
from ecs.core.components.script import Script
from shmup.common.constants import Z_INDEX_STARS


class PlayerCollision(Script):

    def __init__(self, gfx1, gfx2, W, H, entBurst, compName=None):
        super().__init__(compName)
        self._lastHitDuration = 0
        self._gfx1 = gfx1
        self._gfx2 = gfx2
        self._w    = W
        self._h    = H
        self._entBurst = entBurst

    def updateScript(self, scriptName, deltaTime):
        # update last hit
        if self._lastHitDuration < 1:
            self._lastHitDuration += deltaTime
        else:
            # get player positions
            x1,y1 = self._gfx1.getPosition()
            x2,y2 = self._gfx2.getPosition()
            # get inter player dist
            dx  = abs(x1-x2)
            dy  = abs(y1-y2)
            if dx < self._w/2 and dy<self._h/2:
                # There is a collision create a burst emitter
                params  = {"x0"           : (x1+x2)/2,
                           "y0"           : (y1+y2)/2,
                           "partSize"     : 32,
                           "partScale"    : 1.5,
                           "partSpeed"    : 2.0,
                           "color"        : (255, 255, 0),
                           "startAlpha"   : 100,
                           "endAlpha"     : 50,
                           "imagePath"    : "resources/images/items/star.png",
                           "partInterval" : 0.070,
                           "totalDuration": 0.30
                           }
                starBurst = GfxBurstEmitter(self._gfx1.getScene(),params,Z_INDEX_STARS,"starBurst")
                self._entBurst.addComponent(starBurst)
                # reinit timer
                self._lastHitDuration = 0
