from ecs.core.components.script import Script
from shmup.common.constants import SCROLL_SPEED2


class MoveCoin(Script):

    def __init__(self, gfx, downLimit, time, initPos, eCoins, compName="MoveCoin"):
        super().__init__(compName)
        self._limit   = downLimit
        self._gfx     = gfx
        self._timer   = 0
        self._initPos = initPos
        self._timeMax = time
        self._eCoins = eCoins

    def updateScript(self, scriptName, deltaTime):
        toDestroy = []
        #Get coin position
        x, y = self._gfx.getPosition()
        # Move to the left, according to the parallax ("sand") speed
        self._gfx.move((7/10)*SCROLL_SPEED2 * deltaTime * 60, 0)
        # If it has not reached the bottom of the sea...
        if y > self._limit:
            # ... makes it drown
            self._gfx.move(0,-10*deltaTime*60)
        else:
            # ... or stop animation
            self._gfx.pause()
            # Increase time (duration on the sand)
            self._timer += deltaTime
            # If this time has exceeded,
            if self._timer > self._timeMax:
                # Destroy entity
                ent = self._gfx.getEntity()
                if ent != None:
                    toDestroy.append(ent)

        # Destroy if it gets out of the screen
        if x < -self._gfx.getWidth()/2:
            ent = self._gfx.getEntity()
            if ent != None:
                toDestroy.append(ent)

        for ent in toDestroy:
            ent.destroy()
            self._eCoins.remove(ent)
