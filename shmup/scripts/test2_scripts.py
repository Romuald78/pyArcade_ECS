from ecs.components.script import Script


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
        self.gfx.setPosition((500, self.life.getValue()*80 + 80))


class MoveStick(Script):

    def __init__(self, sprite, axisX, axisY, compName=None):
        super().__init__(compName)
        # store components
        self.gfx   = sprite
        self.xAxis = axisX
        self.yAxis = axisY

    def updateScript(self, scriptName, deltaTime):
        # set the Y value of the sprite to the life value * COEF
        self.gfx.setPosition((300*self.xAxis.getValue()+1200, -300*self.yAxis.getValue()+500))


class SelectScene(Script):

    def __init__(self, scn, key, compName=None):
        super().__init__(compName)
        # store components
        self.scene = scn
        self.key   = key

    def updateScript(self, scriptName, deltaTime):
        if self.key.hasBeenPressed():
            self.scene.selectNewScene("TEST2")


