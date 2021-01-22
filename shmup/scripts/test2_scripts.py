from ecs.core.components.script import Script


class ModifLife(Script):

    def __init__(self, buttonUp, buttonDown, lifeComp, compName=None):
        super().__init__(compName)
        # store components
        self.life = lifeComp
        self.up   = buttonUp
        self.down = buttonDown

    def updateScript(self, scriptName, deltaTime):
        if self.up.hasBeenPressed():
            self.life.modify(1)
        if self.down.hasBeenPressed():
            self.life.modify(-1)


class MoveGfx(Script):

    def __init__(self, sprite, lifeComp, compName=None):
        super().__init__(compName)
        # store components
        self.gfx  = sprite
        self.life = lifeComp

    def updateScript(self, scriptName, deltaTime):
        # set the Y value of the sprite to the life value * COEF
        self.gfx.setPosition((1025, self.life.getValue()*70 + 80))


class MoveStick(Script):

    def __init__(self, sprite, axisX, axisY, compName=None):
        super().__init__(compName)
        # store components
        self.gfx   = sprite
        self.xAxis = axisX
        self.yAxis = axisY

    def updateScript(self, scriptName, deltaTime):
        # set the Y value of the sprite to the life value * COEF
        self.gfx.setPosition((300*self.xAxis.getValue()+1075, -300*self.yAxis.getValue()+500))


class PauseScene(Script):

    def __init__(self, scn, key, compName=None):
        super().__init__(compName)
        # store components
        self.scene = scn
        self.key   = key

    def updateScript(self, scriptName, deltaTime):
        if self.key.hasBeenPressed():
            if self.scene.isPaused():
                self.scene.resume()
            else:
                self.scene.pause()

class ShowHidePanda(Script):

    def __init__(self, keyPlus, keyMinus, keyVis, gfxComp, compName=None):
        super().__init__(compName)
        # store components
        self.keyAdd = keyPlus
        self.keySub = keyMinus
        self.keyVis = keyVis
        self.gfx    = gfxComp

    def updateScript(self, scriptName, deltaTime):
        if self.keyVis.hasBeenPressed():
            if self.gfx.isVisible():
                self.gfx.hide()
            else:
                self.gfx.show()

        if self.keyAdd.hasBeenPressed():
            newZ = self.gfx.getZIndex()-11
            self.gfx.setZIndex(newZ)
        if self.keySub.hasBeenPressed():
            newZ = self.gfx.getZIndex()+11
            self.gfx.setZIndex(newZ)
