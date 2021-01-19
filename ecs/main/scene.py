
## ============================================================
## IMPORTS
## ============================================================
from ecs.main.world import World



## ============================================================
## SCENE class (extended by the user userScenes)
## ============================================================
class Scene():

    ## -------------------------------------
    ## Constructor
    ## -------------------------------------
    def __init__(self):
        self.__world = World(self)


    ## -------------------------------------
    ## Entity management
    ## -------------------------------------
    def addEntity(self,nam, ref):
        self.__world.addEntity(nam, ref)


    ## -------------------------------------
    ## Gfx Component management
    ## -------------------------------------
    def setVisible(self, gfxComp, val):
        self.__world.gfxMgr.setVisible(gfxComp.getGfx(), val)
    def isVisible(self, gfxComp):
        return self.__world.gfxMgr.isVisible(gfxComp.getGfx())


    ## -------------------------------------
    ## Main methods
    ## -------------------------------------
    def update(self, deltaTime):
        self.__world.update(deltaTime)

    def draw(self):
        self.__world.draw()


    ## -------------------------------------
    ## Notify inputs
    ## -------------------------------------
    def onKeyEvent(self,key, isPressed):
        self.__world.onKeyEvent(key, isPressed)

    def onMouseButtonEvent(self, buttonName, x, y, isPressed):
        self.__world.onMouseButtonEvent(buttonName, x, y, isPressed)

    def onMouseMotionEvent(self, x, y, dx, dy):
        self.__world.onMouseMotionEvent(x, y, dx, dy)

    def onGamepadButtonEvent(self, gamepadId, buttonName, isPressed):
        self.__world.onGamepadButtonEvent(gamepadId, buttonName, isPressed)

    def onGamepadAxisEvent(self, gamepadId, axisName, analogValue):
        self.__world.onGamepadAxisEvent(gamepadId, axisName, analogValue)


    ## -------------------------------------
    ## Get transition times and colors
    ## -------------------------------------
    def getTransitionTimeIN(self):
        return 1.0

    def getTransitionTimeOUT(self):
        return 1.0

    def getTransitionColorIN(self):
        return (0,255,0)

    def getTransitionColorOUT(self):
        return (255,0,0)


