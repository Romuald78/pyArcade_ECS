from ecs.core.components.script import Script


class DestroyPlayer(Script):

    def __init__(self, lifeComp, playerEnt, compName=None):
        super().__init__(compName)
        self._life = lifeComp
        self._ent = playerEnt
        self._destroyed = False

    def updateScript(self, scriptName, deltaTime):
        if not self._destroyed:
            if self._life.getValue()<=0:
             self._ent.destroy()

