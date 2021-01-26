from ecs.core.components.idle import Idle


class Fox(Idle):

    def __init__(self, initGfx, compName=None):
        if compName == None:
            compName = "FOX"
        super().__init__(compName)
        self._foxGfx = initGfx

    def getFox(self):
        return self._foxGfx

    def setFox(self, newFoxGfx):
        self._foxGfx = newFoxGfx


