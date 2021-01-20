
## ============================================================
## IMPORTS
## ============================================================
import arcade

from ecs.main.world import World



## ============================================================
## SCENE class (extended by the user userScenes)
## ============================================================
class Scene():

    ## -------------------------------------
    ## Constructor
    ## -------------------------------------
    def __init__(self, W, H):
        self._world = World(self)
        self._consoleDebug = False
        self._drawDebug    = False
        self._dimensions   = (W,H)


    ## -------------------------------------
    ## Entity management
    ## -------------------------------------
    def addEntity(self,ref):
        self._world.addEntity(ref)
    def getEntitiesByName(self, entNam):
        return self._world.getEntitiesByName(entNam)
    def getNbEntities(self):
        return self._world.getNbEntities()
    def getEntityList(self):
        return self._world.getAllEntities()


    ## -------------------------------------
    ## Gfx Component management
    ## -------------------------------------
    def setVisible(self, gfxComp, val):
        self._world._gfxMgr.setVisible(gfxComp.getGfx(), val)
    def isVisible(self, gfxComp):
        return self._world._gfxMgr.isVisible(gfxComp.getGfx())


    ## -------------------------------------
    ## Main methods
    ## -------------------------------------
    def update(self, deltaTime):
        self._world.update(deltaTime)

    def draw(self):
        self._world.draw()


    ## -------------------------------------
    ## Notify inputs
    ## -------------------------------------
    def onKeyEvent(self,key, isPressed):
        self._world.onKeyEvent(key, isPressed)

    def onMouseButtonEvent(self, buttonName, x, y, isPressed):
        self._world.onMouseButtonEvent(buttonName, x, y, isPressed)

    def onMouseMotionEvent(self, x, y, dx, dy):
        self._world.onMouseMotionEvent(x, y, dx, dy)

    def onGamepadButtonEvent(self, gamepadId, buttonName, isPressed):
        self._world.onGamepadButtonEvent(gamepadId, buttonName, isPressed)

    def onGamepadAxisEvent(self, gamepadId, axisName, analogValue):
        self._world.onGamepadAxisEvent(gamepadId, axisName, analogValue)


    ## -------------------------------------
    ## DEBUG
    ## -------------------------------------
    def getDimensions(self):
        return self._dimensions
    def setDebugMode(self, consoleDebug, drawDebug):
        self._consoleDebug = consoleDebug
        self._drawDebug    = drawDebug
    def displayDebugInfo(self):
        if self._consoleDebug:
            msg = "Your scene has no 'displayDebugInfo' method implemented yet !"
            print(msg)
    def drawDebugInfo(self):
        if self._drawDebug:
            msg = "Your scene has no 'drawDebugInfo' method implemented yet !"
            arcade.draw_text(msg, 20, self._dimensions[1]-20, (255,255,255), 12)


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


