from shmup.common.constants import SCREEN_WIDTH
from ecs.components.script import Script

class MoveAnalog(Script):

    def __init__(self, gfx, xAxis, spd, disappear=None, visMove=None, isLeft=True):
        super().__init__()
        self.gfx           = gfx
        self.xAxis         = xAxis
        self.speed         = spd
        self.dis           = disappear
        self.isVisibleMove = visMove
        self.isLeft = isLeft

    def updateScript(self, action, deltaTime):
        val = self.xAxis.getValue()
        prev = self.xAxis.getLastValue()

        self.gfx.move(self.speed*val*60*deltaTime, 0)
        pos = self.gfx.getPosition()
        if pos[0] < 75:
            self.gfx.setPosition((75,pos[1]))
        if pos[0] > SCREEN_WIDTH-75:
            self.gfx.setPosition((SCREEN_WIDTH-75, pos[1]))

            # if the references are not None
        if self.dis != None:
            if self.isVisibleMove != None:
                # Moving
                if abs(val) > 0:
                    newVis = self.isVisibleMove
                    if (self.isLeft and val>0) or (not self.isLeft and val<0):
                        newVis = False
                else :
                    newVis = not self.isVisibleMove
                    if (self.isLeft and prev>0) or (not self.isLeft and prev<0):
                        newVis = False
                # update newVis according to show
                if not self.dis.isShowing():
                    newVis = False
                # use final result
                self.gfx.setVisible(newVis)


class Disappear(Script):
    def __init__(self, button):
        super().__init__()
        self.button = button
        self.showing = True

    def isShowing(self):
        return self.showing

    def updateScript(self, action, deltaTime):
        if self.button.hasBeenPressed():
            self.showing = not self.showing
