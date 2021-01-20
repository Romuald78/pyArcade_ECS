# TODO Add remove entity method + all the links with the different systems


from ecs.components.component import Component
from ecs.systems.gfxSystem import GfxSystem
from ecs.systems.idleSystem import IdleSystem
from ecs.systems.inputSystem import InputSystem
from ecs.systems.scriptSystem import ScriptSystem


class World():

    ## -------------------------------------
    ## Constructor
    ## -------------------------------------
    def __init__(self, scn):
        # attach scene to this world
        self._scene = scn
        # Create systems
        self._inputMgr  = InputSystem()
        self._gfxMgr    = GfxSystem()
        self._scriptMgr = ScriptSystem()
        self._idleMgr   = IdleSystem()
        # prepare entity dict
        self._entByName = {}
        self._entByRef  = {}


    ## -------------------------------------
    ## Register component to systems
    ## -------------------------------------
    def _registerComponent(self, compRef):
        # Retrieve component type and check before registering to systems
        compType = compRef.getType()
        # SCRIPT component
        if compType == Component.TYPE_SCRIPT:
            # TODO check component is well added into the system | 1
            self._scriptMgr.add(compRef)
        # INPUT KEYBOARD component
        elif compType == Component.TYPE_KEYBOARD:
            key    = compRef.getKey()
            action = compRef.getActionName()
            # TODO check component is well added into the system |
            self._inputMgr.registerKey(key, action, compRef)
        # INPUT GAMEPAD BUTTON component
        elif compType == Component.TYPE_GAMEPAD_BUTTON:
            ctrlID = compRef.getGamepadID()
            button = compRef.getButton()
            action = compRef.getActionName()
            # TODO check component is well added into the system |
            self._inputMgr.registerButton(ctrlID, button, action, compRef)
        # INPUT MOUSE BUTTON component
        elif compType == Component.TYPE_MOUSE_BUTTON:
            button = compRef.getButton()
            action = compRef.getActionName()
            # TODO check component is well added into the system |
            self._inputMgr.registerClick(button, action, compRef)
        # INPUT MOUSE MOTION component
        elif compType == Component.TYPE_MOUSE_MOTION:
            action = compRef.getActionName()
            # TODO check component is well added into the system |
            self._inputMgr.registerMouse(action, compRef)
        # INPUT GAMEPAD AXIS component
        elif compType == Component.TYPE_GAMEPAD_AXIS:
            ctrlID = compRef.getGamepadID()
            axis = compRef.getAxis()
            action = compRef.getActionName()
            # TODO check component is well added into the system |
            self._inputMgr.registerAxis(ctrlID, axis, action, compRef)
        # GFX components
        elif (compType & Component.TYPE_GFX_MASK) == Component.TYPE_GFX_MASK:
            z = compRef.getZIndex()
            vis = True
            # TODO check component is well added into the system |
            self._gfxMgr.registerGfx(compRef, z, vis)
        # USER components
        elif compType == Component.TYPE_USER:
            # TODO check component is well added into the system |
            self._idleMgr.add(compRef)
        else:
            raise ValueError(f"[ERR] addEntity : unknow component type {compType} !")


    ## -------------------------------------
    ## Entity management
    ## -------------------------------------
    def addEntity(self,entRef):
        # retrieve entity name
        entName = entRef.getName()
        # Store entity by Name
        if not entName in self._entByName:
            self._entByName[entName] = []
        if entRef in self._entByName[entName]:
            raise ValueError("[ERR] addEntity : reference is already in the name dict !")
        self._entByName[entName].append(entRef)
        # Store entity by ref
        if entRef in self._entByRef:
            raise ValueError("[ERR] addEntity : reference is already in the ref dict !")
        self._entByRef[entRef] = entName

        # Get all entity components from entity (dict by ref)
        comps = entRef.getComponentList()
        for compRef in comps:
            # Register this component to the corresponding system
            self._registerComponent(compRef)

    def getNbEntities(self):
        return len(self._entByRef)

    def getEntitiesByName(self,entName):
        res = []
        if entName in self._entByName:
            res = self._entByName[entName]
        return res

    def hasEntity(self, entRef):
        return entRef in self._entByRef

    def getAllEntities(self):
        return list(self._entByRef.keys())


    ## -------------------------------------
    ## Main methods
    ## -------------------------------------
    def update(self, deltaTime):
        self._scriptMgr.updateAllScripts(deltaTime)
        self._gfxMgr.updateAllGfx(deltaTime)

    def draw(self):
        self._gfxMgr.drawAllGfx()


    ## -------------------------------------
    ## Input event methods
    ## -------------------------------------
    def onKeyEvent(self,key, isPressed):
        self._inputMgr.notifyKeyEvent(key, isPressed)

    def onMouseButtonEvent(self, buttonName, x, y, isPressed):
        self._inputMgr.notifyMouseButtonEvent(buttonName, x, y, isPressed)

    def onMouseMotionEvent(self, x, y, dx, dy):
        self._inputMgr.notifyMouseMotionEvent(x, y, dx, dy)

    def onGamepadButtonEvent(self, gamepadId, buttonName, isPressed):
        self._inputMgr.notifyGamepadButtonEvent(gamepadId, buttonName, isPressed)

    def onGamepadAxisEvent(self, gamepadId, axisName, analogValue):
        self._inputMgr.notifyGamepadAxisEvent(gamepadId, axisName, analogValue)

