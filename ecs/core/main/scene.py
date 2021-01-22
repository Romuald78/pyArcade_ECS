
## ============================================================
## IMPORTS
## ============================================================
import arcade

from ecs.core.main.world import World



## ============================================================
## SCENE class (extended by the idle userScenes)
## ============================================================
class Scene():
    # ---------------------------------------------
    # COMPONENT ID
    # ---------------------------------------------
    # Static field
    _maxSceneID = 0
    @staticmethod
    def getNewID():
        Scene._maxSceneID += 1
        return Scene._maxSceneID


    ## -------------------------------------
    ## Constructor
    ## -------------------------------------
    def __init__(self, scnMgr, W, H, sceneName=None):
        self._sceneMgr     = scnMgr
        self._world        = World(self)
        self._consoleDebug = False
        self._drawDebug    = False
        self._dimensions   = (W,H)
        self._ID = Scene.getNewID()
        if sceneName == None:
            sceneName = "SCENE"
        self._sceneName    = f"s_{sceneName}_{self._ID}"


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
    def notifyUpdateVisible(self, gfxComp):
        self._world._gfxMgr.notifyUpdateVisible(gfxComp)
    def notifyUpdateZIndex(self, gfxComp):
        self._world._gfxMgr.notifyUpdateZIndex(gfxComp)


    ## -------------------------------------
    ## Main methods
    ## -------------------------------------
    def update(self, deltaTime):
        self._world.update(deltaTime, self._sceneMgr.isPaused())

    def draw(self):
        self._world.draw()


    ## -------------------------------------
    ## Scene management
    ## -------------------------------------
    def getName(self):
        return self._sceneName

    def getID(self):
        return self._ID

    def selectNewScene(self, sceneName):
        self._sceneMgr.selectNewScene(sceneName)

    def pause(self):
        self._sceneMgr.pause()

    def resume(self):
        self._sceneMgr.resume()

    def isPaused(self):
        return self._sceneMgr.isPaused()


    ## -------------------------------------
    ## Notify inputs
    ## -------------------------------------
    def onKeyEvent(self,key, isPressed):
        self._world.onKeyEvent(key, isPressed, self._sceneMgr.isPaused())

    def onMouseButtonEvent(self, buttonName, x, y, isPressed):
        self._world.onMouseButtonEvent(buttonName, x, y, isPressed, self._sceneMgr.isPaused())

    def onMouseMotionEvent(self, x, y, dx, dy):
        self._world.onMouseMotionEvent(x, y, dx, dy, self._sceneMgr.isPaused())

    def onGamepadButtonEvent(self, gamepadId, buttonName, isPressed):
        self._world.onGamepadButtonEvent(gamepadId, buttonName, isPressed, self._sceneMgr.isPaused())

    def onGamepadAxisEvent(self, gamepadId, axisName, analogValue):
        self._world.onGamepadAxisEvent(gamepadId, axisName, analogValue, self._sceneMgr.isPaused())


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
            msg = "[INFO] Your scene has no implementation of 'displayDebugInfo' method !"
            print(msg)
    def drawDebugInfo(self):
        if self._drawDebug:
            # arcade.draw_rectangle_filled(self._dimensions[0]//2, self._dimensions[1]//2, self._dimensions[0], self._dimensions[1],(128,128,128,128))
            refX = 15
            refY = self._dimensions[1] - 20
            # Scene information
            a = ["[_]", "[o]"][not self.isPaused()]
            msg = f"{a} {self.getName()}"
            arcade.draw_text(msg, refX, refY, (255,255,255), 14)

            # Scene entities
            entities = self.getEntityList()
            for ent in entities:
                refY = self._dimensions[1] - 38
                arcade.draw_text(ent.getName(), refX+15, refY, (64, 255, 64), 14)
                refY -= 18
                components = ent.getComponentList()
                for comp in components:
                    n = comp.getName()
                    s = comp.getTypeName()
                    c = comp.getTypeColor()
                    a = ["[_]", "[o]"][comp.isEnabled() and (not self.isPaused() or comp.isEnabledOnPause())]
                    msg = f"{a} {n} ({s})"
                    arcade.draw_text(msg, refX + 30, refY, c, 12)
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

