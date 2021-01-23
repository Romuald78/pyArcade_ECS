
from ecs.core.components.component import Component
from ecs.core.systems.gfxSystem import GfxSystem
from ecs.core.systems.idleSystem import IdleSystem
from ecs.core.systems.inputSystem import InputSystem
from ecs.core.systems.scriptSystem import ScriptSystem


class World():

    ## -------------------------------------
    ## CONSTRUCTOR
    ## -------------------------------------
    def __init__(self, scn):
        # attach scene to this world
        self._scene = scn
        # Create systems
        self._inputMgr  = InputSystem()
        self._gfxMgr    = GfxSystem()
        self._scriptMgr = ScriptSystem()
        self._idleMgr   = IdleSystem()


    ## -------------------------------------
    ## COMPONENT REGISTRATION
    ## -------------------------------------
    def _registerComponent(self, compRef):
        # Retrieve component type and check before registering to systems
        compType = compRef.getType()
        # SCRIPT component
        if compType == Component.TYPE_SCRIPT:
            self._scriptMgr.add(compRef)
        # INPUT KEYBOARD component
        elif compType == Component.TYPE_KEYBOARD:
            key    = compRef.getKey()
            action = compRef.getActionName()
            self._inputMgr.registerKey(key, action, compRef)
        # INPUT GAMEPAD BUTTON component
        elif compType == Component.TYPE_GAMEPAD_BUTTON:
            ctrlID = compRef.getGamepadID()
            button = compRef.getButton()
            action = compRef.getActionName()
            self._inputMgr.registerButton(ctrlID, button, action, compRef)
        # INPUT MOUSE BUTTON component
        elif compType == Component.TYPE_MOUSE_BUTTON:
            button = compRef.getButton()
            action = compRef.getActionName()
            self._inputMgr.registerClick(button, action, compRef)
        # INPUT MOUSE MOTION component
        elif compType == Component.TYPE_MOUSE_MOTION:
            action = compRef.getActionName()
            self._inputMgr.registerMouse(action, compRef)
        # INPUT GAMEPAD AXIS component
        elif compType == Component.TYPE_GAMEPAD_AXIS:
            ctrlID = compRef.getGamepadID()
            axis = compRef.getAxis()
            action = compRef.getActionName()
            self._inputMgr.registerAxis(ctrlID, axis, action, compRef)
        # GFX components
        elif (compType & Component.TYPE_GFX_MASK) == Component.TYPE_GFX_MASK:
            self._gfxMgr.registerGfx(compRef)
        # USER components
        elif compType == Component.TYPE_IDLE:
            self._idleMgr.add(compRef)
        else:
            raise ValueError(f"[ERR] addEntity : unknow component type {compType} !")

    def _unregisterComponent(self,cmpRef):
        # TODO finish this service with all comp refs (access to correct system)
        # Remove GFX component from the system
        if (cmpRef.getType() & Component.TYPE_GFX_MASK) == Component.TYPE_GFX_MASK:
            self._gfxMgr.removeGfx(cmpRef)


    ## -------------------------------------
    ## COMPONENT NOTIFICATIONS
    ## -------------------------------------
    def notifyAddComponent(self, cmpRef):
        # Register Gfx component into the system
        self._registerComponent(cmpRef)

    def notifyRemoveComponent(self, cmpRef):
        # Unregister Gfx component kinto the system
        self._unregisterComponent(cmpRef)


    ## -------------------------------------
    ## MAIN METHODS
    ## -------------------------------------
    def update(self, deltaTime, isOnPause):
        self._scriptMgr.updateAllScripts(deltaTime, isOnPause)
        self._gfxMgr.updateAllGfx(deltaTime, isOnPause)

    def draw(self):
        self._gfxMgr.drawAllGfx()


    ## -------------------------------------
    ## INPUT NOTIFICATIONS
    ## -------------------------------------
    def onKeyEvent(self,key, isPressed, isOnPause):
        self._inputMgr.notifyKeyEvent(key, isPressed, isOnPause)
    def onMouseButtonEvent(self, buttonName, x, y, isPressed,isOnPause):
        self._inputMgr.notifyMouseButtonEvent(buttonName, x, y, isPressed,isOnPause)
    def onMouseMotionEvent(self, x, y, dx, dy,isOnPause):
        self._inputMgr.notifyMouseMotionEvent(x, y, dx, dy,isOnPause)
    def onGamepadButtonEvent(self, gamepadId, buttonName, isPressed,isOnPause):
        self._inputMgr.notifyGamepadButtonEvent(gamepadId, buttonName, isPressed,isOnPause)
    def onGamepadAxisEvent(self, gamepadId, axisName, analogValue,isOnPause):
        self._inputMgr.notifyGamepadAxisEvent(gamepadId, axisName, analogValue,isOnPause)

