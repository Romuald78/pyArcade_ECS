from ecs.core.components.idle import Idle


class DirtType(Idle):

    def __init__(self,type,compName=None):
        super().__init__(compName)
        self._type = type

    def getValue(self):
        return self._type