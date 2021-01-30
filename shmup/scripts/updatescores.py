import math

from ecs.core.components.script import Script


class UpdateScores(Script):


    def __init__(self, score, unitGfx, decGfx, hndGfx, compName=None):
        super().__init__(compName)

        self._score = score
        self._u = unitGfx
        self._d = decGfx
        self._h = hndGfx

    def updateScript(self, scriptName, deltaTime):
        # get score
        scr = self._score.getValue()
        scr = f"000{scr}"
        self._u.setTexture(int(scr[-1]))
        self._d.setTexture(int(scr[-2]))
        self._h.setTexture(int(scr[-3]))