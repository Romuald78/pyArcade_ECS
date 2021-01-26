from ecs.core.components.gfx import GfxBurstEmitter
from ecs.core.components.script import Script
from shmup.common.constants import Z_INDEX_STARS


class PlayerCollision(Script):
    def __init__(self, phyWorld, fox, gfx1, gfx2, colTyp1, colTyp2,  entBurst, compName=None):
        # Call to parent
        super().__init__(compName)
        # Store fields
        self._lastHitDuration = 0
        self._entBurst  = entBurst
        self._phyWorld  = phyWorld
        self._gfx1      = gfx1
        self._gfx2      = gfx2
        self._foxRef    = fox
        self._inContact = False
        # Create collision handler
        handler = phyWorld.add_collision_handler(colTyp1, colTyp2)
        handler.data["scriptRef"] = self
        handler.data["gfx1"]      = gfx1
        handler.data["gfx2"]      = gfx2
        print(handler.data)
        handler.begin    = PlayerCollision.beginCollision
        handler.separate = PlayerCollision.endCollision

    @staticmethod
    def beginCollision(arbiter, space, data):
        # Get current script ref
        scriptRef = data["scriptRef"]
        # Get gfx refs
        gfx1 = data["gfx1"]
        gfx2 = data["gfx2"]
        # Check players
        if gfx1 == scriptRef._gfx1 and gfx2 == scriptRef._gfx2:
            scriptRef._inContact = True
        return False

    @staticmethod
    def endCollision(arbiter, space, data):
        # Get current script ref
        scriptRef = data["scriptRef"]
        # Get gfx refs
        gfx1 = data["gfx1"]
        gfx2 = data["gfx2"]
        # Check players
        if gfx1 == scriptRef._gfx1 and gfx2 == scriptRef._gfx2:
            scriptRef._inContact = False
        return False

    def updateScript(self, scriptName, deltaTime):
        # update last hit
        if self._lastHitDuration < 1:
            if not self._inContact:
                self._lastHitDuration += deltaTime
        elif self._inContact:
                x1, y1 = self._gfx1.getPosition()
                x2, y2 = self._gfx2.getPosition()
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
                starBurst = GfxBurstEmitter(params,Z_INDEX_STARS,"starBurst")
                self._entBurst.addComponent(starBurst)
                # reinit timer and collision
                self._lastHitDuration = 0
