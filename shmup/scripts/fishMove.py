import math

from ecs.core.components.script import Script


class FishMove(Script):


    def __init__(self, gfx, spd, ampl, period, compName=None):
        super().__init__(compName)

        self._gfx = gfx
        self._speed = spd
        self._ampl = ampl
        self._period = period
        self._counter = 0

    def updateScript(self, scriptName, deltaTime):
        self._counter += deltaTime*60
        dx = -self._speed*60*deltaTime
        dy = self._ampl*60*deltaTime*math.sin(2*math.pi*self._counter/(60*self._period))
        self._gfx.move( dx, dy )
