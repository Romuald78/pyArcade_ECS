import math

from ecs.core.components.script import Script


class HudLife(Script):


    def __init__(self, life, gfxList, compName=None):
        super().__init__(compName)

        self._gfxs = gfxList
        self._life = life

    def updateScript(self, scriptName, deltaTime):
        lf = self._life.getValue()
        mx = self._life.getMax()
        for i in range(mx,lf,-1):
            self._gfxs[i-1].hide()

