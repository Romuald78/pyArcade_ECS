
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
    def __init__(self, scnMgr, W, H):
        self._sceneMgr     = scnMgr
        self._world        = World(self)
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
    ## Scene management
    ## -------------------------------------
    def selectNewScene(self, sceneName):
        self._sceneMgr.selectNewScene(sceneName)


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
            # arcade.draw_rectangle_filled(self._dimensions[0]//2, self._dimensions[1]//2, self._dimensions[0], self._dimensions[1],(128,128,128,128))
            refX = 15
            entities = self.getEntityList()
            for ent in entities:
                refY = self._dimensions[1] - 20
                arcade.draw_text(ent.getName(), refX, refY, (64, 255, 64), 14)
                refY -= 18
                components = ent.getComponentList()
                for comp in components:
                    n = comp.getName()
                    s = comp.getTypeName()
                    c = comp.getTypeColor()
                    msg = f"{n} ({s})"
                    arcade.draw_text(msg, refX + 10, refY, c, 12)
                    refY -= 15
                # next entity is displayed to the right
                refX += 140

    ## -------------------------------------
    ## Get transition times and colors
    ## -------------------------------------
    def getTransitionTimeIN(self):
        return 1
    def getTransitionTimeOUT(self):
        return 1
    def getTransitionColorIN(self):
        return (0,255,0)
    def getTransitionColorOUT(self):
        return (255,0,0)

