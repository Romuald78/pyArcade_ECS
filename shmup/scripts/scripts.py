from ecs.components.script import Script


class ScrMoveKey(Script):

    def __init__(self, gfx, xAxis, spd):
        self.gfx   = gfx
        self.xAxis = xAxis
        self.speed = spd

    def updateScript(self, action, deltaTime):
        val = self.xAxis.getValue()
        self.gfx.move(self.speed*val*60*deltaTime, 0)

