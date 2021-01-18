from ecs.components.component import Component
from ecs.systems.gfx import GfxSystem
from ecs.systems.input import InputSystem
from ecs.systems.script import ScriptSystem


class World():

    ## -------------------------------------
    ## Constructor
    ## -------------------------------------
    def __init__(self, scn):
        # attach scene to this world
        self.scene = scn
        # Create systems
        self.__inputMgr  = InputSystem()
        self.__gfxMgr    = GfxSystem()
        self.__scriptMgr = ScriptSystem()
        # prepare entity dict
        self.__entities = {}


    ## -------------------------------------
    ## Entity management
    ## -------------------------------------
    def addEntity(self,entName, entRef):
        if not entName in self.__entities:
            self.__entities[entName] = entRef
            # Register all components
            comps = entRef.getAllComponents()
            for compName in comps:
                compRef  = comps[compName]
                compType = compRef.getType()

                # -------------------- SCRIPTS --------------------
                if compType == Component.TYPE_SCRIPT:
                    self.__scriptMgr.add(compName,compRef)

                # -------------------- INPUTS --------------------
                elif compType == Component.TYPE_KEYBOARD:
                    key    = compRef.getKey()
                    action = compRef.getActionName()
                    self.__inputMgr.registerKey(key,action,compRef)

                elif compType == Component.TYPE_GAMEPAD_BUTTON:
                    ctrlID = compRef.getGamepadID()
                    button = compRef.getButton()
                    action = compRef.getActionName()
                    self.__inputMgr.registerButton(ctrlID,button,action,compRef)

                elif compType == Component.TYPE_MOUSE_BUTTON:
                    button = compRef.getButton()
                    action = compRef.getActionName()
                    self.__inputMgr.registerClick(button,action,compRef)

                elif compType == Component.TYPE_MOUSE_MOTION:
                    action = compRef.getActionName()
                    self.__inputMgr.registerMouse(action,compRef)

                elif compType == Component.TYPE_GAMEPAD_AXIS:
                    ctrlID = compRef.getGamepadID()
                    axis   = compRef.getAxis()
                    action = compRef.getActionName()
                    self.__inputMgr.registerAxis(ctrlID,axis,action,compRef)

                # -------------------- GFX --------------------
                elif compType == Component.TYPE_SIMPLE_SPRITE:
                    z   = compRef.getZIndex()
                    vis = True
                    self.__gfxMgr.registerGfx(compRef, z, vis)

                elif compType == Component.TYPE_SIMPLE_LIST:
                    z   = compRef.getZIndex()
                    vis = True
                    self.__gfxMgr.registerGfx(compRef, z, vis)

                # TODO handle other components !!!!!!!!!!!!


    def removeEntity(self, entName):
        if entName in self.__entities:
            del self.__entities[entName]
            # unregister all components
            # TODO
            #

    def getNbEntities(self):
        return len(self.__entities)

    def getEntity(self,entName):
        res = None
        if entName in self.__entities:
            res = self.__entities[entName]
        return res


    ## -------------------------------------
    ## Main methods
    ## -------------------------------------
    def update(self, deltaTime):
        self.__scriptMgr.updateAllScripts(deltaTime)
        self.__gfxMgr.updateAllGfx(deltaTime)

    def draw(self):
        self.__gfxMgr.drawAllGfx()


    ## -------------------------------------
    ## Input event methods
    ## -------------------------------------
    def onKeyEvent(self,key, isPressed):
        self.__inputMgr.notifyKeyEvent(key, isPressed)

    def onMouseButtonEvent(self, buttonName, x, y, isPressed):
        self.__inputMgr.notifyMouseButtonEvent(buttonName, x, y, isPressed)

    def onMouseMotionEvent(self, x, y, dx, dy):
        self.__inputMgr.notifyMouseMotionEvent(x, y, dx, dy)

    def onGamepadButtonEvent(self, gamepadId, buttonName, isPressed):
        self.__inputMgr.notifyGamepadButtonEvent(gamepadId, buttonName, isPressed)

    def onGamepadAxisEvent(self, gamepadId, axisName, analogValue):
        self.__inputMgr.notifyGamepadAxisEvent(gamepadId, axisName, analogValue)


