import math

from ecs.core.components.script import Script


class UpdateScores(Script):


    def __init__(self, score, unitGfx, decGfx, hndGfx, thsGfx, compName=None):
        super().__init__(compName)

        self._score = score
        self._u = unitGfx
        self._d = decGfx
        self._h = hndGfx
        self._t = thsGfx

    def updateScript(self, scriptName, deltaTime):
        # get score
        scr = self._score.getValue()
        scr = f"0000{scr}"
        self._u.setTexture(int(scr[-1]))
        self._d.setTexture(int(scr[-2]))
        self._h.setTexture(int(scr[-3]))
        self._t.setTexture(int(scr[-4]))